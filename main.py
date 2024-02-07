from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from db.session import engine
from db import Base
from routes import v1_router


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(v1_router)


def add_middleware(app) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    print(settings.CORS_ORIGINS)
    print(type(settings.CORS_ORIGINS[0]))


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    add_middleware(app)
    include_router(app)
    return app


app = start_application()


@app.get("/")
async def root():
    return {
        "message": f"Welcome to my {settings.PROJECT_NAME} {settings.PROJECT_VERSION}"
    }
