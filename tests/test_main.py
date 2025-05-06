import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import src.main as main_module
from src.config import config as cfg
import src.aq_mcp_server as server_module

# Initialize TestClient for the FastAPI app
client = TestClient(main_module.app)

def test_app_instance():
    assert hasattr(main_module, "app"), "main module should have `app`"
    assert isinstance(main_module.app, FastAPI)

def test_openapi_servers_url():
    # The OpenAPI spec should include the GROK_URL from config
    openapi = main_module.app.openapi()
    assert "servers" in openapi
    servers = openapi["servers"]
    assert any(s.get("url") == cfg.GROK_URL for s in servers)

def test_messages_docs_route():
    # GET /messages should return 200 and null body
    response = client.get("/messages")
    assert response.status_code == 200
    assert response.json() is None

def test_customers_endpoint(monkeypatch):
    # Stub the underlying tool to return predictable data
    monkeypatch.setattr(server_module, "get_customers_by_email", lambda email: [{"id": 1}])
    response = client.get("/aquarium/customers", params={"email": "x@y.com"})
    assert response.status_code == 200
    assert response.json() == [{"id": 1}]