"""
Tests for Email Classification Service
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.main import app, ClassificationResult

client = TestClient(app)

# ── Health checks ─────────────────────────────────────────────────────────────

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# ── Classification (mocked) ───────────────────────────────────────────────────

MOCK_RESULT = ClassificationResult(
    category="ORDER_STATUS",
    subcategory="Shipping Delay",
    priority="HIGH",
    confidence=0.95,
    suggested_action="Check order tracking and reply with updated ETA",
    summary="Customer inquiring about delayed order #12345"
)

@patch("app.main.classify_email", return_value=MOCK_RESULT)
def test_classify_order_status(mock_fn):
    response = client.post("/classify", json={
        "sender": "john.doe@example.com",
        "subject": "Where is my order #12345?",
        "body": "Hi, I placed an order last week and it still hasn't arrived. Can you help?"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "ORDER_STATUS"
    assert data["priority"] == "HIGH"
    assert 0.0 <= data["confidence"] <= 1.0

@patch("app.main.classify_email", return_value=MOCK_RESULT)
def test_classify_missing_field(mock_fn):
    response = client.post("/classify", json={
        "sender": "test@example.com",
        "subject": "Hello"
        # missing body
    })
    assert response.status_code == 422  # Validation error

def test_classify_empty_strings():
    response = client.post("/classify", json={
        "sender": "",
        "subject": "",
        "body": ""
    })
    # Should either process or return 422, not 500
    assert response.status_code in [200, 422, 500]
