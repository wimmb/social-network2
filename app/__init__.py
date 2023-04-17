from flask import Flask
from config import Config
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import datetime


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # install extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .user import bp as user_bp
    app.register_blueprint(user_bp)

    from .post import bp as post_bp
    app.register_blueprint(post_bp)

    from .faker import bp as fake_bp
    app.register_blueprint(fake_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp)

    from . import models # noqa

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(user_id)

    @app.context_processor
    def context_processor():
        return dict(
            current_user=current_user
        )

    return app


app = create_app()


@app.before_request
def before_request():
    if current_user.is_authenticated:
        if current_user.profile:
            current_user.profile.last_seen = datetime.utcnow()
            db.session.commit()
