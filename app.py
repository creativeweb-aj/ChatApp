from dotenv import load_dotenv
from flask_cors import CORS

# To load environment variables
load_dotenv()
from flask import Flask
from config.extension import db, ma, migrate, socketio
from src.UserApp.view import UserApi
from src.ChatApp.view import ChatApi


# Flask App initialize with extensions and run
def create_app():
    # Flask app initialize
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_pyfile('config/configurations.py')

    # Blueprints
    app.register_blueprint(UserApi, url_prefix='/auth')
    app.register_blueprint(ChatApi, url_prefix='/chat')

    # Database connection initialize
    db.init_app(app)

    # Marshmallow initialize
    ma.init_app(app)

    # Database migrate initialize
    migrate.init_app(app, db, render_as_batch=False, compare_type=True)

    socketio.init_app(app, cors_allowed_origins='*')
    # Return App for run in run.py file
    return app


# Run Application
if __name__ == "__main__":
    socketio.run(app=create_app(), allow_unsafe_werkzeug=True, debug=True, host='0.0.0.0', port=5001)
