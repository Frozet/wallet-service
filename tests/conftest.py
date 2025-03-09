import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client