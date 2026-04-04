import pytest
from app.models.user import Role
from app.models.transaction import TransactionType

def test_login(client, test_users):
    response = client.post("/api/v1/auth/login", data={"username": "admin@test.com", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_admin_transaction_flow_and_filtering(client, auth_headers):
    headers = auth_headers("admin")
    t1 = client.post("/api/v1/transactions/", headers=headers, json={"amount": 500, "type": "income", "category": "salary"})
    assert t1.status_code == 200, t1.json()
    t2 = client.post("/api/v1/transactions/", headers=headers, json={"amount": 100, "type": "expense", "category": "groceries"})
    assert t2.status_code == 200
    res_filter = client.get("/api/v1/transactions/?type=expense", headers=headers)
    assert res_filter.status_code == 200
    assert len(res_filter.json()["items"]) == 1
    assert res_filter.json()["items"][0]["category"] == "groceries"