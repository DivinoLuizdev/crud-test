from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Config do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://admin:admin123@flask_postgres:5432/produtosdb'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # 👇 Importa modelos *depois* de criar db/app
    from app.model.models import Product

    # Importa e registra rotas
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
