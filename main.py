from fastapi import FastAPI
from config import settings

# from dependencies import get_query_token
from config.database import Base, engine, SessionLocal
from config.routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    contact=settings.APP_CONTACT_INFO,
    license_info=settings.APP_LICENSE_INFO
)

app.include_router(router)
