from flask import Flask
from config import Config
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # install extensions
    db.init_app(app)
    migrate.init_app(app, db)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .models import User

    @app.context_processor
    def context_processor():
        return dict(
            current_user=current_user
        )

    return app


app = create_app()
from .main import routes
