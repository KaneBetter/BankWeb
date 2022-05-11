import logging
import sqlalchemy
import hashlib
from flask import Blueprint, render_template, flash, redirect, request, session, url_for, escape
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm as Form
from wtforms import StringField, DecimalField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError, NumberRange

from bank import models, exceptions

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    target = request.args.get("target")
    if target:
        logger.info("target: {}".format(target))
    if request.method == 'GET':
        return render_template('login.html', form=form)

    if not form.validate_on_submit():
        for name, msgs in form.errors.items():
            for msg in msgs:
                logger.error("Error: " + name + "-" + msg)
        return redirect(url_for("index.index"))

    else:
        try:
            user = models.User.find_user(form.username.data,
                                         hashlib.sha256(form.password.data.encode('utf-8')).hexdigest(), )
            login_user(user, remember=form.remember.data)  # If the checkbox in the form is selected
            print('Logged in successfully.')
        except exceptions.UserDoesNotExistOrWrongPassword:
            flash('Wrong username or password!')
            # return render_template('login.html', form=form)
            return redirect(url_for("auth.login"))
        target = request.args.get("target")
        if target is not None:
            logger.info(("Login redirect:", target))
            return redirect(target)
        return redirect(url_for("index.index"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    # For Post method.
    if form.validate_on_submit():
        user: models.User
        try:
            user = models.User.create_user(
                form.username.data,
                hashlib.sha256(form.password.data.encode('utf-8')).hexdigest(),
                escape(form.email.data),
                balance=form.balance.data
            )
        except sqlalchemy.exc.IntegrityError:
            flash("The username exists. Please try another one.")
            logger.info("UsernameExist: {}".format(form.username.data))
            return render_template('register.html', form=form)
        login_user(user)
        return redirect(url_for("index.index"))
    else:
        for name, msgs in form.errors.items():
            for msg in msgs:
                logger.error(("Error:" + name + "-" + msg))
                flash(f'{name} error: {msg}')
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successfully.', 'info')
    return redirect(url_for("auth.login"))


class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = StringField(validators=[DataRequired()])
    remember = BooleanField(default=True)


class RegisterForm(Form):
    username = StringField(validators=[
        DataRequired(),
        Length(min=1, max=127),
        Regexp(r'^[a-z0-9_\-\.]+$', message='Username invalid.')
    ])
    password = StringField(validators=[
        DataRequired()
        #Length(min=1, max=127),
        #Regexp(r'^[a-z0-9_\-\.]+$', message='Password invalid.')
    ])
    retyped_pwd = StringField(validators=[
        DataRequired(),
        EqualTo('password', message='Password does not match.')
    ])
    email = StringField(validators=[Email()])
    balance = DecimalField(validators=[
        DataRequired(),
        NumberRange(min=0.00, max=4294967295.99, message='Balance overflow.')
    ])
