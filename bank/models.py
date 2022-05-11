import logging
from datetime import datetime

import sqlalchemy
from decimal import Decimal
from flask_login import UserMixin
from bank import exceptions, constants
from bank.extensions import db

logger = logging.getLogger(__name__)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), unique=True, nullable=False, )
    password = db.Column(db.String(127), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.FLOAT, nullable=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    db.extend_existing = True

    @staticmethod
    def create_user(username: str, password: str, email: str, balance: Decimal) -> 'User':
        # Create user here.
        try:
            user = User(username=username,
                        password=password,
                        email=email,
                        balance=balance)
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as ex:
            db.session.rollback()
            raise ex

        return user

    @staticmethod
    def find_user(username: str, password: str) -> 'User':
        user = User.query.filter_by(username=username).first()
        print(username + " " + password)
        if user is None:
            raise exceptions.UserDoesNotExistOrWrongPassword()
        logger.info((username + " " + password, user.password, user.username))
        if user.password != password:
            raise exceptions.UserDoesNotExistOrWrongPassword()

        return user


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default=datetime.now(), index=True)
    amount = db.Column(db.Integer, nullable=False)

    @staticmethod
    def user_trans(userid: str) -> 'Transaction':
        trans = Transaction.query.filter_by(userid=userid).order_by(Transaction.id.desc()).limit(10).all()
        return trans
