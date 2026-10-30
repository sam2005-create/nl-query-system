import pytest

import db
from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_NAME", str(tmp_path / "test.db"))
    db.init_db()
    return app.test_client()


def test_query_returns_columns_and_rows(client):
    res = client.post("/query", json={"query": "average marks of cse students"})
    assert res.status_code == 200
    body = res.get_json()
    assert body["columns"] == ["average_marks"]
    assert len(body["rows"]) == 1


def test_question_it_cant_parse(client):
    res = client.post("/query", json={"query": "tell me a joke"})
    assert res.status_code == 400
    assert "couldn't understand" in res.get_json()["error"]


def test_empty_query(client):
    res = client.post("/query", json={"query": "   "})
    assert res.status_code == 400
