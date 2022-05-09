import logging

from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user

from bank import models, constants, db
from bank.models import Transaction

logger = logging.getLogger(__name__)
tranx_bp = Blueprint('transcation', __name__)

@tranx_bp.route("/deposit", methods=["POST","GET"])
def deposit():
    if request.method == 'GET':
        return redirect(url_for("index.index"))

    owner_id = current_user.id
    user = models.User.query.get(owner_id)
    # TODO 检测 form.validate() 和 user not null
    logger.info(("id:", owner_id, "user:", user))
    logger.info(("request.form", request.form))
    amount = int(request.form.get('amount'))
    user.balance += amount
    record = Transaction(userid=owner_id, amount=amount)
    db.session.add(record)
    if user.balance > constants.MAX_BALANCE:
        flash("Ooops. You have too much money.")
        db.session.rollback()
    db.session.commit()
    return redirect(url_for("index.index"))

@tranx_bp.route("/withdraw", methods=["POST", "GET"])
def withdraw():
    if request.method == 'GET':
        return redirect(url_for("index.index"))

    owner_id = current_user.id
    user = models.User.query.get(owner_id)
    # TODO 检测 form.validate() 和 user not null
    logger.info(("id:", owner_id, "user:", user))
    logger.info(("request.form", request.form))
    amount = int(request.form.get('amount'))
    user.balance -= amount
    record = Transaction(userid=owner_id, amount=-amount)
    db.session.add(record)
    if user.balance < 0:
        flash("Ooops. You don't have that amount of money.")
        db.session.rollback()
    db.session.commit()
    return redirect(url_for("index.index"))
