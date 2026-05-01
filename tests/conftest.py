import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
from app.oauth2 import create_access_token
from app import models

# Ensure you are targeting port 5433 to punch through the local dev mount
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@localhost:5433/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    # Annihilate existing tables to ensure absolute sterility
    models.Base.metadata.drop_all(bind=engine) # type: ignore
    
    # Reconstruct the schema with fully registered models
    models.Base.metadata.create_all(bind=engine) # type: ignore
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "swbanga@unhinged.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "sayed_trap@unhinged.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "DevSecOps Phase 1", "content": "Mastering Linux", "owner_id": test_user['id']},
        {"title": "DevSecOps Phase 2", "content": "Mastering Postgres", "owner_id": test_user['id']},
        {"title": "DevSecOps Phase 3", "content": "Mastering Docker", "owner_id": test_user2['id']}
    ]
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    session.query(models.Post).all()
    return posts