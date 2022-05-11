import logging

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm as Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp
from bank import models

from bank import models

index_bp = Blueprint('index', __name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@index_bp.route("/")
@login_required
def index():
    form = TransactionForm()
    trans = models.Transaction.user_trans(current_user.id)
    print(trans)
    logger.debug(("see the current:", current_user))
    return render_template("index.html", form=form, data=trans)


class TransactionForm(Form):
    amount = StringField(validators=[DataRequired(),
        Regexp("^(0|[1-9][0-9]*){1}(\.[0-9]{2})?$", message="Invalid input.")])
