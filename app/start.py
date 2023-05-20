
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from app.views.article import articlesViews, backOffice, homePage, adminConnect
from app.core.myconfig import settings, secretKeyMiddleware
from starlette.middleware.sessions import SessionMiddleware

# création instance fastAPI
app = FastAPI(title="Mercadona 1.0")

# création de la route public vers fichiers statiques CSS/JS/
app.mount("/public", StaticFiles(directory=settings.STATIC_FILES_DIR), name="public")   
app.add_middleware(SessionMiddleware, secret_key=secretKeyMiddleware.key_MDLW)

register_tortoise(
    app,
    db_url=settings.POSTGRESQL_URL,
    modules={"models": settings.TORTOISE_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)

#### inclure APIRouters catalogue public / backoffice privé
app.include_router(homePage)
app.include_router(articlesViews)
app.include_router(backOffice)    
app.include_router(adminConnect)