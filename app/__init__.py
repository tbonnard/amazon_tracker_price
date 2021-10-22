from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.views import login_manager
    login_manager.init_app(app)

    from app.views import bootstrap
    bootstrap.init_app(app)

    from app.views import main
    app.register_blueprint(main)

    return app


import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from .script import script_check_price_users

scheduler = BackgroundScheduler()
scheduler.add_job(func=script_check_price_users, trigger="interval", seconds=86400)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())