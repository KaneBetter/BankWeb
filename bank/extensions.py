from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


login_manager = LoginManager()
bootstrap = Bootstrap4()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    from bank.models import User
    # TODO 这里user_id可能不是int，可以注入
    return User.query.get(user_id)