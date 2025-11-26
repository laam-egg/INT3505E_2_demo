from pymongo.collection import Collection
from .MessageQueueService import MessageQueueService
from ..BaseCRUDService import BaseCRUDService
from ...utils.pageable import Pageable
from typing import override
from flask_restx import abort
import validators
from ...utils.log import log
import threading

class WebhookService(BaseCRUDService):
    def __init__(self,
        collection: Collection,
        mq_service: MessageQueueService,
        delivery_queue: str = "delivery_queue",
        report_queue: str = "report_queue",
    ) -> None:
        super().__init__(collection)
        self.mq = mq_service
        self.delivery_queue = delivery_queue
        self.report_queue = report_queue

        # Ensure queues exist
        self.mq.declare_queue(self.delivery_queue)
        self.mq.declare_queue(self.report_queue)

        # Start background thread to consume report_queue
        threading.Thread(target=self._consume_in_background, daemon=True).start()
    
    def _consume_in_background(self):
        mq = self.mq.clone() # since: each thread must have its own MQ connection, otherwise: pika.exceptions.StreamLostError: Stream connection lost: IndexError('pop from an empty deque')
        # Ensure queues exist
        mq.declare_queue(self.delivery_queue)
        mq.declare_queue(self.report_queue)
        # Register callback for report_queue
        mq.register_callback(self.report_queue, self._process_report_event)
        # Start consumption
        mq.start_consuming()
    
    def _process_report_event(self, message: dict):
        """
        Internal callback for each event from the report_queue.
        Expects message to contain:
        {
            "eventName": str,
            "targetUrl": str,
            "success": bool,
            "timestamp": int
        }
        """
        try:
            event_name = message.get("eventName", None)
            if event_name is None:
                raise ValueError("eventName is required in report event")
            target_url = message.get("targetUrl", None)
            if target_url is None:
                raise ValueError("targetUrl is required in report event")
            success = message.get("success", None)
            if success is None:
                raise ValueError("success is required in report event")
            timestamp = message.get("timestamp", None)
            if timestamp is None:
                raise ValueError("timestamp is required in report event")
            
            log.info(f"Received delivery report: Event '{event_name}' to {target_url} at {timestamp} -> {'SUCCESS' if success else 'FAILURE'}")
        except Exception as e:
            log.error(f"Failed to process report event: {e}")
    
    @override
    def post_item(self, item_doc):
        targetUrl = item_doc.get("targetUrl", None)
        if not targetUrl:
            abort(400, "targetUrl là bắt buộc")  # type: ignore
        if not validators.url(targetUrl):
            abort(400, "targetUrl không hợp lệ")  # type: ignore
        
        eventName = item_doc.get("eventName", None)
        if not eventName:
            abort(400, "eventName là bắt buộc")  # type: ignore

        # IT'S NOT: return super().post_item(item_doc)
        # IDEMPOTENCY => upsert

        result = self.collection.replace_one(
            {
                "eventName": eventName,
                "targetUrl": targetUrl,
            },
            item_doc,
            upsert=True,
        )

        id = result.upserted_id
        if id is None:
            # Existing document was replaced, need to find its _id
            existing_doc = self.collection.find_one({
                "eventName": eventName,
                "targetUrl": targetUrl,
            })
            if existing_doc:
                id = existing_doc.get("_id", None)
        
        return {
            "_id": id,
            **item_doc
        }

    def get_collection_by_targetUrl(
        self, targetUrl: str | None, pageable: Pageable
    ):
        """
        Tìm và trả về danh sách các webhooks theo URL đích,
        có pagination.

        Nếu targetUrl trống thì không lọc theo targetUrl nữa.
        """
        q = {}
        if targetUrl:
            q['targetUrl'] = targetUrl

        return [
            *self.collection.find(
                q,
                **pageable.get_kwargs()
            )
        ]
    
    def _delete_item_by_eventName_and_targetUrl(self, eventName: str, targetUrl: str):
        result = self.collection.delete_many({
            "eventName": eventName,
            "targetUrl": targetUrl,
        })
        log.info(f"Deleted {result.deleted_count} webhook(s) for event '{eventName}' and targetUrl '{targetUrl}'")
        return result.deleted_count
    
    def propagate_event(self, event_name: str, event_content: dict, target_urls: list[str] | None = None):
        """
        Gửi một sự kiện đến tất cả các webhook đã đăng ký.
        (Bất đồng bộ, không hoàn thành task ngay lập tức.)
        """
        message = {
            "eventName": event_name,
            "eventContent": event_content,
        }
        if target_urls is not None:
            message["targetUrls"] = target_urls
        self.mq.publish_message(self.delivery_queue, message)
