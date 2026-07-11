"""
File test đơn giản cho app_web.py
Chạy bằng lệnh: pytest -v
"""
import pytest
from app_web import app

# Bật chế độ testing của Flask (tắt debug, tránh side-effect)
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

"""Trang chủ phải trả về HTTP 200 (không lỗi)."""
def test_homepage_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200

"""Trang chủ phải hiển thị đủ 2 thông tin quan trọng: trạng thái và container ID."""
def test_homepage_contains_key_info(client):
    response = client.get("/")
    html = response.data.decode("utf-8")

    assert "Trạng thái" in html
    assert "Container ID" in html