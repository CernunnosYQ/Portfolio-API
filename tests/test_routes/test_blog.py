from tests.utils.user import create_test_user

data = {"title": "This is my title", "content": "This is my content"}


def test_get_blogpost(client, db_session):
    _, token = create_test_user(db=db_session)
    create_bp_response = client.post(
        "/v1/create/blog", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert create_bp_response.status_code == 201

    blogpost = create_bp_response.json()

    not_found_response = client.get("/v1/get/blog/99999")
    assert not_found_response.status_code == 404

    get_bp_response = client.get(f"/v1/get/blog/{blogpost['id']}")
    assert get_bp_response.status_code == 200

    response_data = get_bp_response.json()
    assert response_data["title"] == data["title"]
    assert response_data["content"] == data["content"]


def test_update_blogpost(client, db_session):
    _, token = create_test_user(db=db_session)
    old_post = client.post(
        "/v1/create/blog", json=data, headers={"Authorization": f"Bearer {token}"}
    ).json()

    new_data = {"title": "This is my new title", "content": "This is my new content"}

    not_found_response = client.put(
        "/v1/update/blog/99999",
        json=new_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert not_found_response.status_code == 404

    unauthorized_response = client.put(
        "/v1/update/blog/99999",
        json=new_data,
        headers={"Authorization": "Bearer bad token"},
    )
    assert unauthorized_response.status_code == 400

    update_response = client.put(
        f"/v1/update/blog/{old_post.get('id')}",
        json=new_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_response.status_code == 200

    response_data = update_response.json()
    assert response_data["title"] == new_data["title"]
    assert response_data["title"] != old_post["title"]
    assert response_data["content"] != old_post["content"]


def test_delete_blog(client, db_session):
    _, token = create_test_user(db=db_session)
    post = client.post(
        "/v1/create/blog", json=data, headers={"Authorization": f"Bearer {token}"}
    ).json()

    not_found_response = client.delete(
        "/v1/delete/blog/99999", headers={"Authorization": f"Bearer {token}"}
    )
    assert not_found_response.status_code == 404

    delete_response = client.delete(
        f"/v1/delete/blog/{post.get('id')}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200

    response_data = delete_response.json()
    assert response_data["message"]
