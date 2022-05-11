import logging

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm as Form
from wtforms import IntegerField
from wtforms.validators import DataRequired

from bank import models

index_bp = Blueprint('index', __name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@index_bp.route("/")
@login_required
def index():
    form = TransactionForm()
    logger.debug(("see the current:", current_user))
    owner_id = current_user.id
    user = models.User.query.get(owner_id)
    data = {'username': user.username, 'balance': user.balance, 'mail': user.email}
    return render_template("index.html", form=form, data=data)


class TransactionForm(Form):
    amount = IntegerField(validators=[DataRequired()])
