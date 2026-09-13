from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def disable_background_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    """API tests focus on HTTP/CRUD; metadata is tested separately."""
    monkeypatch.setattr(
        "later_api.api.resources.fetch_and_save_metadata",
        MagicMock(),
    )


def test_create_resource(client: TestClient) -> None:
    response = client.post(
        "/resources",
        json={"url": "https://example.com/article"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["url"] == "https://example.com/article"
    assert data["title"] is None
    assert data["source_id"] is None
    assert data["status"] == "unread"


def test_get_resources_empty(client: TestClient) -> None:
    response = client.get("/resources")

    assert response.status_code == 200
    assert response.json() == []


def test_get_resource_by_id(client: TestClient) -> None:
    created = client.post(
        "/resources",
        json={"url": "https://example.com/one"},
    ).json()

    response = client.get(f"/resources/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["url"] == "https://example.com/one"


def test_get_resource_not_found(client: TestClient) -> None:
    response = client.get("/resources/999")

    assert response.status_code == 404


def test_edit_resource(client: TestClient) -> None:
    created = client.post(
        "/resources",
        json={"url": "https://example.com/edit-me"},
    ).json()

    response = client.patch(
        f"/resources/{created['id']}",
        json={"title": "My title", "status": "read"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "My title"
    assert data["status"] == "read"


def test_edit_resource_not_found(client: TestClient) -> None:
    response = client.patch(
        "/resources/999",
        json={"title": "Nope"},
    )

    assert response.status_code == 404


def test_delete_resource(client: TestClient) -> None:
    created = client.post(
        "/resources",
        json={"url": "https://example.com/delete-me"},
    ).json()

    delete_response = client.delete(f"/resources/{created['id']}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"ok": True}

    get_response = client.get(f"/resources/{created['id']}")
    assert get_response.status_code == 404


def test_delete_resource_not_found(client: TestClient) -> None:
    response = client.delete("/resources/999")

    assert response.status_code == 404


def test_filter_resources_by_status(client: TestClient) -> None:
    unread = client.post(
        "/resources",
        json={"url": "https://example.com/unread"},
    ).json()
    read = client.post(
        "/resources",
        json={"url": "https://example.com/read"},
    ).json()
    client.patch(f"/resources/{read['id']}", json={"status": "read"})

    response = client.get("/resources", params={"status": "read"})

    assert response.status_code == 200
    ids = [item["id"] for item in response.json()]
    assert read["id"] in ids
    assert unread["id"] not in ids


def test_filter_resources_by_category_id(client: TestClient) -> None:
    category = client.post("/categories", json={"name": "filter-me"}).json()
    with_category = client.post(
        "/resources",
        json={"url": "https://example.com/in-category"},
    ).json()
    without_category = client.post(
        "/resources",
        json={"url": "https://example.com/no-category"},
    ).json()
    client.patch(
        f"/resources/{with_category['id']}",
        json={"category_id": category["id"]},
    )

    response = client.get(
        "/resources",
        params={"category_id": category["id"]},
    )

    assert response.status_code == 200
    ids = [item["id"] for item in response.json()]
    assert with_category["id"] in ids
    assert without_category["id"] not in ids


def test_filter_resources_by_source_id(client: TestClient) -> None:
    first = client.post(
        "/resources",
        json={"url": "https://example.com/source-a"},
    ).json()
    second = client.post(
        "/resources",
        json={"url": "https://example.com/source-b"},
    ).json()
    client.patch(f"/resources/{first['id']}", json={"source_id": 42})

    response = client.get("/resources", params={"source_id": 42})

    assert response.status_code == 200
    ids = [item["id"] for item in response.json()]
    assert first["id"] in ids
    assert second["id"] not in ids
