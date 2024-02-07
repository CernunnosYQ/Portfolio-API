data = {
    "username": "testuser",
    "email": "testuser@test.com",
    "password": "TestUser123456",
}


def test_create_user(client):
    response = client.post("/v1/create/user", json=data)
    assert response.status_code == 201

    response_data = response.json()
    assert response_data["email"] == data["email"]
    assert response_data["username"] == data["username"]
    assert response_data["is_active"]


def test_get_by_email(client):
    client.post("/v1/create/user", json=data)
    response = client.get(f"/v1/get/user/{data['email']}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["email"] == data["email"]
    assert response_data["username"] == data["username"]


def test_get_by_username(client):
    client.post("/v1/create/user", json=data)
    response = client.get(f"/v1/get/user/{data['username']}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["email"] == data["email"]
    assert response_data["username"] == data["username"]
