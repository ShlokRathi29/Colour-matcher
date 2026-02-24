from __future__ import annotations

from flask import Flask
from flask_cors import CORS

from config import AppConfig
from src.core.shade_database import ShadeDatabase
from src.core.matcher import BirlaOpusMatcher
from src.api.routes import create_routes


def create_app() -> Flask:
    cfg = AppConfig()

    db = ShadeDatabase(cfg.shades_lab_csv)
    db.load()

    matcher = BirlaOpusMatcher(db)

    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = cfg.max_upload_mb * 1024 * 1024

    # ENABLE CORS ON THE REAL APP
    CORS(app)

    app.register_blueprint(create_routes(matcher), url_prefix="/api")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False)
