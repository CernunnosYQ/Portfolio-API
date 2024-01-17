from tests.utils.user import create_test_user

data = {"title": "This is my title", "content": "This is my content"}


def test_create_blogpost(client, db_session):
    _ = create_test_user(db=db_session)
    response = client.post("/v1/blogs", json=data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == data["title"]
    assert response_data["content"] == data["content"]


def test_get_blogpost(client, db_session):
    _ = create_test_user(db=db_session)
    blogpost = client.post("/v1/blogs", json=data).json()

    response = client.get(f"/v1/blogs/{blogpost['id']}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == data["title"]
    assert response_data["content"] == data["content"]
