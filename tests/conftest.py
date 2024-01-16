from typing import Any, Generator

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings  # noqa: E402
from routes import v1_router  # noqa: E402
from db.session import get_db  # noqa: E402
from db import Base  # noqa: E402


def start_application():
    app = FastAPI()
    app.include_router(v1_router)
    return app


TESTING_DB_URL = "/".join(settings.DB_URL.split("/")[:-1]) + "/testing"

engine = create_engine(TESTING_DB_URL)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    "Create a fresh db on each test case"

    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses "db_session" fixture to override
    'get_db' dependency injected into routes
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
