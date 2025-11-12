from ...db import (
    patrons_collection,
    titles_collection,
    copies_collection,
    borrows_collection,
    users_collection,
    payments_collection,
)

from ...services.v2 import *

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
user_service = UserService(
    collection=users_collection,
)
