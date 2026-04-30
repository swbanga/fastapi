import pytest
from jose import jwt
from app.config import settings

def test_create_user(client):
    res = client.post("/users/", json={"email": "newuser@test.com", "password": "password123"})
    assert res.status_code == 201
    assert res.json().get("email") == "newuser@test.com"

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    assert res.status_code == 200
    token = res.json().get("access_token")
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert res.json().get("token_type") == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('swbanga@unhinged.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('swbanga@unhinged.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code