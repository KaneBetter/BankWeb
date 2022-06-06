import datetime
import logging

from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user

from bank import models, constants, db
from bank.index import TransactionForm
from bank.models import Transaction

logger = logging.getLogger(__name__)
tranx_bp = Blueprint('transcation', __name__)

@tranx_bp.route("/deposit", methods=["POST","GET"])
def deposit():
    if request.method == 'GET':
        return redirect(url_for("index.index"))
    form = TransactionForm()
    if not form.validate_on_submit():
        logger.error(("Not valid deposit request", form))
        flash("Not a valid deposit request.")
        return redirect(url_for("index.index"))
    owner_id = current_user.id
    user = models.User.query.get(owner_id)
    if not user:
        return redirect(url_for("index.index"))
    logger.info(("id:", owner_id, "user:", user))
    logger.info(("request.form", request.form))
    amount = form.amount.data
    logger.debug(("Type of amoubnt:", amount))
    try:
        amount = float(amount)
    except ValueError as e:
        flash("Invalid input")
        logger.error(("Error:", e))
        return redirect(url_for("index.index"))
    user.balance += amount
    user.balance = round(user.balance, 2)
    record = Transaction(userid=owner_id, amount=amount, timestamp=datetime.datetime.now())
    db.session.add(record)
    # if user.balance > constants.MAX_BALANCE:
    #     flash("Ooops. You have too much money.")
    #     db.session.rollback()
    db.session.commit()
    return redirect(url_for("index.index"))

@tranx_bp.route("/withdraw", methods=["POST", "GET"])
def withdraw():
    if request.method == 'GET':
        return redirect(url_for("index.index"))
    form = TransactionForm()
    if not form.validate_on_submit():
        logger.error(("Not valid withdraw request", form))
        return redirect(url_for("index.index"))
    owner_id = current_user.id
    user = models.User.query.get(owner_id)
    # TODO 检测 form.validate() 和 user not null
    logger.info(("id:", owner_id, "user:", user))
    logger.info(("request.form", request.form))
    amount = request.form.get('amount')
    try:
        amount = float(amount)
    except ValueError as e:
        flash("Invalid input")
        logger.error(("Error:", e))
        return redirect(url_for("index.index"))
    user.balance -= amount
    user.balance = round(user.balance, 2)
    record = Transaction(userid=owner_id, amount=-amount, timestamp=datetime.datetime.now())
    db.session.add(record)
    if user.balance < 0:
        flash("Ooops. You don't have that amount of money.")
        db.session.rollback()
    db.session.commit()
    return redirect(url_for("index.index"))
