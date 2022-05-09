from datetime import datetime

import sqlalchemy
from decimal import Decimal
from flask_login import UserMixin
from bank import exceptions, constants
from bank.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, )
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer, nullable=False)
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
            print(user)
            raise exceptions.UserDoesNotExistOrWrongPassword()
        if user.password != password:
            raise exceptions.UserDoesNotExistOrWrongPassword()

        return user

    # 似乎不需要了这两个函数
    def deposit(self, amount: Decimal):
        self.balance += amount
        if self.balance > constants.MAX_BALANCE:
            db.session.rollback()
            raise exceptions.BalanceOverflow()
        db.session.commit()

    def withdraw(self, amount: Decimal):
        self.balance -= amount
        if self.balance < 0:
            db.session.rollback()
            raise exceptions.BalanceOverflow()
        db.session.commit()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    amount = db.Column(db.Integer, nullable=False)