from pydantic import BaseSettings
import os
from fastapi.templating import Jinja2Templates

dir_path = os.path.dirname(os.path.realpath(__file__))

db_password = os.environ.get('DB_PASSWORD')
user: str = 'franck-r_bddmerca'
host: str = 'postgresql-franck-r.alwaysdata.net'
port: str = '5432'
dbname: str = 'franck-r_mercadona'

############ init ORM tortoise connexion BDD et templates jinja2 ##############

class Settings(BaseSettings):
    APP_NAME: str = "mercadona"
    APP_VERSION: str = "1.0.0"
    POSTGRESQL_URL: str = f"postgres://{user}:{db_password}@{host}:{port}/{dbname}"

    TORTOISE_MODELS = [
        "app.models.article"
    ]

    TEMPLATES_DIR = os.path.join(dir_path, "..", "templates")
    STATIC_FILES_DIR = os.path.join(dir_path, "..", "..", "public")

settings = Settings()

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)