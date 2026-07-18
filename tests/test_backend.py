import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add jarvis-backend directory to the python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "jarvis-backend"))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "JARVIS Backend" in data["message"]

def test_config():
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "JARVIS"

def test_chat():
    response = client.post("/api/chat", json={"message": "hello"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data

def test_screenshot():
    response = client.post("/api/screenshot?analyze=false")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_context():
    response = client.get("/api/context")
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data

def test_browser():
    response = client.post("/api/tools/browser?query=pytest")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data

def test_filesystem():
    # Test create file
    response = client.post("/api/tools/filesystem?operation=create&path=test_file.txt&content=hello_unit_test")
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Test read file
    response = client.post("/api/tools/filesystem?operation=read&path=test_file.txt")
    assert response.status_code == 200
    assert response.json()["content"] == "hello_unit_test"

    # Test delete file
    response = client.post("/api/tools/filesystem?operation=delete&path=test_file.txt")
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_terminal():
    response = client.post("/api/tools/terminal?command=echo%20123&validate_only=true")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "validated" in data
