from tests.utils.user import create_test_user

data = {"title": "This is my title", "content": "This is my content"}


def test_get_blogpost(client, db_session):
    _, token = create_test_user(db=db_session)
    create_bp_response = client.post(
        "/v1/blogs", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert create_bp_response.status_code == 201

    blogpost = create_bp_response.json()

    get_bp_response = client.get(f"/v1/blogs/{blogpost['id']}")
    assert get_bp_response.status_code == 200

    response_data = get_bp_response.json()
    assert response_data["title"] == data["title"]
    assert response_data["content"] == data["content"]
