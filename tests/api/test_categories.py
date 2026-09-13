from fastapi.testclient import TestClient


def test_create_category(client: TestClient) -> None:
    response = client.post("/categories", json={"name": "articles"})

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "articles"


def test_get_categories_empty(client: TestClient) -> None:
    response = client.get("/categories")

    assert response.status_code == 200
    assert response.json() == []


def test_get_category_by_id(client: TestClient) -> None:
    created = client.post("/categories", json={"name": "videos"}).json()

    response = client.get(f"/categories/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["name"] == "videos"


def test_get_category_not_found(client: TestClient) -> None:
    response = client.get("/categories/999")

    assert response.status_code == 404


def test_edit_category(client: TestClient) -> None:
    created = client.post("/categories", json={"name": "old-name"}).json()

    response = client.patch(
        f"/categories/{created['id']}",
        json={"name": "new-name"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "new-name"


def test_edit_category_not_found(client: TestClient) -> None:
    response = client.patch("/categories/999", json={"name": "Nope"})

    assert response.status_code == 404


def test_delete_category(client: TestClient) -> None:
    created = client.post("/categories", json={"name": "temp"}).json()

    delete_response = client.delete(f"/categories/{created['id']}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"ok": True}

    get_response = client.get(f"/categories/{created['id']}")
    assert get_response.status_code == 404


def test_delete_category_not_found(client: TestClient) -> None:
    response = client.delete("/categories/999")

    assert response.status_code == 404


def test_assign_category_to_resource(client: TestClient) -> None:
    category = client.post("/categories", json={"name": "reading"}).json()
    resource = client.post(
        "/resources",
        json={"url": "https://example.com/post"},
    ).json()

    response = client.patch(
        f"/resources/{resource['id']}",
        json={"category_id": category["id"]},
    )

    assert response.status_code == 200
    assert response.json()["category_id"] == category["id"]
