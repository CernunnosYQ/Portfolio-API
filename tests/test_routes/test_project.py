from tests.utils.user import create_test_user

data = {"title": "Portfolio", "description": "New portfolio API"}


def test_get_project(client, db_session):
    _, token = create_test_user(db=db_session)
    create_project_response = client.post(
        "/v1/projects", json=data, headers={"Authorization": f"Bearer {token}"}
    )
    assert create_project_response.status_code == 201

    create_response_data = create_project_response.json()
    get_project_response = client.get(f"/v1/project/{create_response_data.get('id')}")
    assert get_project_response.status_code == 200
    assert data["title"] == get_project_response.json().get("title")


def test_update_project(client, db_session):
    _, token = create_test_user(db=db_session)
    old_project = client.post(
        "/v1/projects", json=data, headers={"Authorization": f"Bearer {token}"}
    ).json()

    new_data = {
        "title": "This is my new title",
        "description": "This is my new description",
    }

    not_found_response = client.put(
        "/v1/project/99999", json=new_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert not_found_response.status_code == 404

    unauthorized_response = client.put(
        "/v1/project/99999",
        json=new_data,
        headers={"Authorization": "Bearer bad token"},
    )
    assert unauthorized_response.status_code == 400

    update_response = client.put(
        f"/v1/project/{old_project.get('id')}",
        json=new_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_response.status_code == 200

    response_data = update_response.json()
    assert response_data["title"] == new_data["title"]
    assert response_data["title"] != old_project["title"]
    assert response_data["description"] != old_project["description"]


def test_delete_project(client, db_session):
    _, token = create_test_user(db=db_session)
    project = client.post(
        "/v1/projects", json=data, headers={"Authorization": f"Bearer {token}"}
    ).json()

    not_found_response = client.delete(
        "/v1/project/99999", headers={"Authorization": f"Bearer {token}"}
    )
    assert not_found_response.status_code == 404

    delete_response = client.delete(
        f"/v1/project/{project.get('id')}", headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 200

    response_data = delete_response.json()
    assert response_data["message"]
