from typing import Literal

def main(mode: Literal['master'] | Literal['slave']):
    from .db import webhooks_collection
    from .services import (
        WebhookService,
        MessageQueueService,
        EventDeliveryService,
    )
    
    webhook_service = WebhookService(collection=webhooks_collection)

    message_queue_service = MessageQueueService()

    event_delivery_service = EventDeliveryService(
        mode=mode,
        mq_service=message_queue_service,
        webhook_service=webhook_service,
    )

    event_delivery_service.start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2 or sys.argv[1] not in ['master', 'slave']:
        print("Usage: python -m app [master|slave]")
        sys.exit(1)
    
    main(mode=sys.argv[1]) # type: ignore
