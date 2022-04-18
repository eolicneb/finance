from sqlalchemy import exc
from settings import PAYMODES
from models import PayMode, db


def insert_pay_modes():
    paymodes = [PayMode(mode=mode) for mode in PAYMODES]
    [db.session.add(paymode) for paymode in paymodes]
    try:
        db.session.commit()
        print("Pay modes inserted in db")
    except exc.IntegrityError:
        db.session.rollback()
