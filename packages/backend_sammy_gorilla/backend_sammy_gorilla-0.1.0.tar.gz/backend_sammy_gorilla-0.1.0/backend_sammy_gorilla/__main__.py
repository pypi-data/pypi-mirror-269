from dotenv import load_dotenv
load_dotenv()
from flask import jsonify, request, Response
from flask_cors import CORS
import os

from backend_sammy_gorilla import create_app
from backend_sammy_gorilla.config.cloudinary_config import configure_cloudinary, fetch_store_pictures, retrieve_pictures
from backend_sammy_gorilla.routes.health import health_bp
from backend_sammy_gorilla.routes.gallery import gallery_bp

app = create_app()
CORS(app, expose_headers='X-Total-Count')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

configure_cloudinary()
# fetch_store_pictures(cursor)

app.register_blueprint(health_bp)
app.register_blueprint(gallery_bp)


base_host = os.getenv("BASE_ADDRESS")

if __name__ == "__main__":
    app.run(host=base_host)
