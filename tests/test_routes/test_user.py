def test_create_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "TestUser123456",
    }

    response = client.post("/v1/users", json=data)
    assert response.status_code == 201

    response_data = response.json()
    assert response_data["email"] == data["email"]
    assert response_data["username"] == data["username"]
    assert response_data["is_active"]
