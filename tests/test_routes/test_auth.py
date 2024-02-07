from tests.utils.user import create_test_user
from core.security import validate_access_token

data = {
    "username": "testuser",
    "email": "testuser@test.com",
    "password": "TestUser123456",
}


def test_create_token(db_session):
    user, token = create_test_user(db_session)
    assert len(token) > 0, "Token is not created"

    validation = validate_access_token(token)
    assert validation.get("success"), "Token validation fails"
    assert validation.get("payload").get("sub") == user.username


def test_email_login(client, db_session):
    user, _ = create_test_user(db_session, data=data)
    response = client.post(
        "/v1/create/token", data={"username": user.email, "password": data["password"]}
    )
    assert response.status_code == 200

    response_data = response.json()
    assert "access_token" in response_data
    assert validate_access_token(response_data.get("access_token")).get("success")
    assert response_data.get("token_type") == "bearer"


def test_username_login(client, db_session):
    user, _ = create_test_user(db_session, data=data)
    response = client.post(
        "/v1/create/token",
        data={"username": user.username, "password": data["password"]},
    )
    assert response.status_code == 200

    response_data = response.json()
    assert "access_token" in response_data
    assert validate_access_token(response_data.get("access_token")).get("success")
    assert response_data.get("token_type") == "bearer"
