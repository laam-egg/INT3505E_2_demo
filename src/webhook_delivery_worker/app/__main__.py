from .db import webhooks_collection
from .services import (
    WebhookService,
    MessageQueueService,
    EventDeliveryService,
)

def main():
    webhook_service = WebhookService(collection=webhooks_collection)

    message_queue_service = MessageQueueService()

    event_delivery_service = EventDeliveryService(
        mq_service=message_queue_service,
        webhook_service=webhook_service,
    )

    event_delivery_service.start()

if __name__ == "__main__":
    main()
