from dotenv import load_dotenv
from flask import Flask
import os

from .yd.routes import yd_bp
from .transcriber.routes import transcriber_bp

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "dev")
    )

    app.register_blueprint(yd_bp)
    app.register_blueprint(transcriber_bp)

    return app
