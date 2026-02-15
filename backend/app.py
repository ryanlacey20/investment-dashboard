from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from routes.auth import auth_bp
from services.token_store import init_db
from routes.portfolio import portfolio_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    init_db()

    app.register_blueprint(portfolio_bp)
    app.register_blueprint(auth_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
