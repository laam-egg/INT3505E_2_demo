from .LogService import LogService
from .WebhookService import WebhookService
from .MessageQueueService import MessageQueueService
import time
import requests
from typing import Literal

class EventDeliveryService:
    """
    Responsible for delivering events to subscribers via HTTP POST.
    Reports success/failure back to backend via MessageQueueService.
    """
    def __init__(self,
        mode: Literal['master'] | Literal['slave'],
        mq_service: MessageQueueService,
        webhook_service: WebhookService,
        delivery_queue: str = "delivery_queue",
        delivery_master_to_slave_queue: str = "delivery_master_to_slave_queue",
        report_queue: str = "report_queue",
    ):
        """
        delivery_queue: Queue name to consume events from backend, for delivery.
        report_queue: Queue name to publish delivery reports, to backend.
        delivery_master_to_slave_queue: Queue name for communication between master and slave processes of the webhook delivery worker.
        """

        self.mode = mode

        self.log = LogService("[EventDeliveryService]")
        self.mq = mq_service
        self.webhook_service = webhook_service
        self.delivery_queue = delivery_queue
        self.report_queue = report_queue
        self.delivery_master_to_slave_queue = delivery_master_to_slave_queue

        # Ensure queues exist
        self.mq.declare_queue(self.delivery_queue)
        self.mq.declare_queue(self.report_queue)
        self.mq.declare_queue(delivery_master_to_slave_queue)

        if self.mode == 'master':
            # Register callback for delivery_queue
            self.mq.register_callback(self.delivery_queue, self._process_delivery_event)
        elif self.mode == 'slave':
            # Register callback for delivery_master_to_slave_queue
            self.mq.register_callback(delivery_master_to_slave_queue, self._process_slave_event)

    def _send_to_webhook(self, target_url: str, event_name: str, event_content: dict) -> bool:
        """
        Sends a single event to a subscriber webhook URL.
        """
        try:
            response = requests.post(
                target_url,
                json={
                    "eventName": event_name,
                    "eventContent": event_content,
                },
                timeout=15
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            self.log.error(f"Failed to deliver event '{event_name}' to {target_url}: {e}")
        except Exception as e:
            self.log.error(f"Unexpected error delivering event '{event_name}' to {target_url}: {e}")
        return False

    def _report_result(self, event_name: str, target_url: str, success: bool):
        """
        Reports delivery result back to backend via report_queue.
        """
        try:
            report = {
                "eventName": event_name,
                "targetUrl": target_url,
                "success": success,
                "timestamp": int(time.time())
            }
            self.mq.publish_message(self.report_queue, report)
            self.log.info(f"Reported delivery result of event `{event_name}`: {target_url} -> {'SUCCESS' if success else 'FAILURE'}")
        except:
            self.log.exception()
            return False
        return True
    
    def _forward_webhook_to_slave(self, target_url: str, event_name: str, event_content: dict):
        """
        Forwards the webhook information to slaves for actual delivery.
        """
        try:
            message = {
                "eventName": event_name,
                "eventContent": event_content,
                "targetUrl": target_url,
            }
            self.mq.publish_message(
                self.delivery_master_to_slave_queue,
                message,
            )
        except:
            self.log.exception()
            return False
        return True

    def _process_delivery_event(self, message: dict):
        """
        Internal callback for each event from the delivery_queue.
        Expects message structure:
        {
            "eventName": "...",
            "eventContent": { ... },
            "targetUrls": [ "...", "...", ... ]  # optional
        }
        """
        try:
            event_name = message.get("eventName")
            if not event_name:
                raise ValueError("Message missing eventName")
            
            event_content = message.get("eventContent")
            if not isinstance(event_content, dict):
                raise ValueError("eventContent must be a dict")
            
            target_urls: list[str] | None = message.get("targetUrls", None)
            if isinstance(target_urls, list):
                target_urls = [ str(url) for url in target_urls ]
            elif target_urls is not None:
                raise ValueError("targetUrls must be a list or None")

            PAGE_SIZE = 50
            page = 1

            while True:
                webhooks = self.webhook_service.get_collection_by_eventName_and_targetUrl(
                    eventName=event_name,
                    targetUrls=target_urls,
                    page=page,
                    size=PAGE_SIZE
                )

                if not webhooks or len(webhooks) == 0:
                    break

                for webhook in webhooks:
                    target_url = webhook.get("targetUrl")
                    if not target_url:
                        self.log.error(f"Webhook missing targetUrl: {webhook}")
                        continue

                    self._forward_webhook_to_slave(
                        target_url=target_url,
                        event_name=event_name,
                        event_content=event_content,
                    )

                page += 1
        except:
            self.log.exception()

    def _process_slave_event(self, message: dict):
        """
        Internal callback for each event from the delivery_master_to_slave_queue.
        Expects message structure:
        {
            "eventName": "...",
            "eventContent": { ... },
            "targetUrl": "..."
        }
        """
        try:
            event_name = message.get("eventName")
            if not event_name:
                raise ValueError("Message missing eventName")
            
            event_content = message.get("eventContent")
            if not isinstance(event_content, dict):
                raise ValueError("eventContent must be a dict")
            
            target_url = message.get("targetUrl")
            if not target_url:
                raise ValueError("Message missing targetUrl")

            success = self._send_to_webhook(
                target_url=target_url,
                event_name=event_name,
                event_content=event_content,
            )

            self._report_result(
                event_name=event_name,
                target_url=target_url,
                success=success,
            )
        except:
            self.log.exception()

    def start(self):
        self.mq.start_consuming()
