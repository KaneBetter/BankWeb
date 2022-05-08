import logging

from flask import Blueprint, request, redirect, url_for
from flask_login import current_user

from bank import models, constants, db, exceptions
from bank.models import Transaction

logger = logging.getLogger(__name__)
tranx_bp = Blueprint('transcation', __name__)

@tranx_bp.route("/deposit", methods=["POST"])
def deposit():
    owner_id = current_user.id
    user = models.User.query.get(owner_id)
    logger.info(("id:", owner_id, "user:", user))
    logger.info(("request.form", request.form))
    amount = int(request.form.get('amount'))
    user.balance += amount
    record = Transaction(userid=owner_id, amount=amount)
    db.session.add(record)
    if user.balance > constants.MAX_BALANCE:
        db.session.rollback()
        raise exceptions.BalanceOverflow()
    db.session.commit()
    return redirect(url_for("index.index"))

@tranx_bp.route("/withdraw", methods=["POST"])
def withdraw():

    pass
