import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_and_read_todo():
    # 1. Создание задачи и чтение
    response = client.post("/todos/", json={"title": "Test task", "description": "Desc"})
    assert response.status_code == 201
    todo = response.json()
    todo_id = todo["id"]
    r_get = client.get(f"/todos/{todo_id}")
    assert r_get.status_code == 200
    assert r_get.json()["title"] == "Test task"
    assert r_get.json()["description"] == "Desc"

def test_update_todo():
    # 2. Обновление задачи и проверка изменений
    create = client.post("/todos/", json={"title": "To update", "description": ""})
    todo_id = create.json()["id"]
    update = client.put(f"/todos/{todo_id}", json={
        "title": "Updated title", "description": "New Desc"
    })
    assert update.status_code == 200
    data = update.json()
    assert data["title"] == "Updated title"
    assert data["description"] == "New Desc"

def test_delete_todo():
    # 3. Удаление задачи и проверка, что она пропала
    create = client.post("/todos/", json={"title": "To delete", "description": ""})
    todo_id = create.json()["id"]
    del_resp = client.delete(f"/todos/{todo_id}")
    assert del_resp.status_code == 204
    r_get = client.get(f"/todos/{todo_id}")
    assert r_get.status_code == 404

def test_read_todo_not_found():
    # 4. Ошибочный запрос несуществующей задачи
    response = client.get("/todos/999999")
    assert response.status_code == 404

def test_create_todo_missing_fields():
    # 5. Ошибка на создание с пропущенными обязательными полями
    response = client.post("/todos/", json={"description": "no title"})
    assert response.status_code == 422  # не прошла валидация