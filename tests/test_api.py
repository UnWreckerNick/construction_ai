from unittest.mock import Mock

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import create_tables, delete_tables, SessionLocal


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    await create_tables()
    yield
    await delete_tables()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def session():
    async with SessionLocal() as s:
        yield s


@pytest.mark.asyncio
async def test_create_project(client, mocker):
    mocker.patch("app.services.model.generate_content", return_value=Mock(text="Task1"))

    response = await client.post("/projects/", json={"project_name": "Mall", "location": "New York"})
    print("Response status:", response.status_code)
    print("Response text:", response.text)
    print("Response JSON:", response.json())
    assert response.status_code == 200, f"Failed with: {response.text}"
    data = response.json()
    assert data["project_name"] == "Mall"
    assert data["location"] == "New York"
    assert "tasks" in data
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["name"] == "Task1"
    assert data["tasks"][0]["status"] == "pending"


@pytest.mark.asyncio
async def test_get_project(client, mocker):
    mocker.patch("app.services.model.generate_content", return_value=Mock(text="Task1"))

    create_response = await client.post("/projects/", json={"project_name": "Bridge", "location": "Chicago"})
    print("Create response status:", create_response.status_code)
    print("Create response text:", create_response.text)
    assert create_response.status_code == 200, f"Failed with: {create_response.text}"
    project_id = create_response.json()["id"]

    get_response = await client.get(f"/projects/{project_id}/")
    print("Get response status:", get_response.status_code)
    print("Get response text:", get_response.text)
    assert get_response.status_code == 200, f"Failed with: {get_response.text}"
    data = get_response.json()
    assert data["id"] == project_id
    assert data["project_name"] == "Bridge"
    assert data["location"] == "Chicago"
    assert len(data["tasks"]) == 1


@pytest.mark.asyncio
async def test_project_not_found(client):
    response = await client.get("/projects/9999/")
    print("Response status:", response.status_code)
    print("Response text:", response.text)
    assert response.status_code == 404, f"Failed with: {response.text}"
    assert response.json()["detail"] == "Project not found"