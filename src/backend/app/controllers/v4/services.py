from ...db import (
    patrons_collection,
    titles_collection,
    copies_collection,
    borrows_collection,
    users_collection,
    payments_collection,
    webhooks_collection,
)

from ...services.v2 import (
    PatronService,
    TitleService,
    CopyService,
    BorrowService,
    PaymentService,
)

borrow_service = BorrowService(
    collection=borrows_collection,
)
copy_service = CopyService(
    collection=copies_collection,
    borrow_service=borrow_service,
)
payment_service = PaymentService(
    collection=payments_collection,
)
patron_service = PatronService(
    collection=patrons_collection,
    payment_service=payment_service,
)
title_service = TitleService(
    collection=titles_collection,
    copy_service=copy_service,
)

from ...services.v3 import (
    MessageQueueService,
    WebhookService,
    UserService,
)

message_queue_service = MessageQueueService()
webhook_service = WebhookService(
    collection=webhooks_collection,
    mq_service=message_queue_service,
)
user_service = UserService(
    collection=users_collection,
    webhook_service=webhook_service,
)
