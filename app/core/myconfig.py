from pydantic import BaseSettings
import os
from fastapi.templating import Jinja2Templates
from decouple import config
import boto3

class S3:
    # bucket s3 amazon
    s3_client = boto3.client('s3')
    bucket_name:str = config("S3_BUCKET_NAME")

#chargement des variables locales pour connexion BDD
db_password: str = config("DB_PASSWORD")
user: str = config("DB_USER")

host: str = 'postgresql-franck-r.alwaysdata.net'
port: str = '5432'
dbname: str = 'franck-r_mercadona'

dir_path = os.path.dirname(os.path.realpath(__file__))

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

class secretKeyMiddleware:
    key_MDLW: str = config("SECRET_MIDDLEWARE")