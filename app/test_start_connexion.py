from app.start import app, register_tortoise
from app.core.myconfig import settings
from tortoise import exceptions as e

def test_connect():

    try:
        register_tortoise(app,
                          db_url=settings.POSTGRESQL_URL,
                          modules={"models": settings.TORTOISE_MODELS},
                          add_exception_handlers=True,
        )
    except (e.ConfigurationError, e.DBConnectionError):
        print("No connection") 