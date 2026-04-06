# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ✅ TEST 1: Home route
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Mini PaaS Backend Running 🚀"}


# ✅ TEST 2: Logs route returns list
def test_logs_returns_list():
    response = client.get("/logs")
    assert response.status_code == 200
    assert "logs" in response.json()
    assert isinstance(response.json()["logs"], list)


# ✅ TEST 3: Deploy with valid repo returns started status
def test_deploy_valid_repo():
    response = client.post("/deploy", json={
        "repo_url": "https://github.com/heroku/python-getting-started"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "Deployment started 🚀"


# ✅ TEST 4: Deploy with empty URL
def test_deploy_empty_url():
    response = client.post("/deploy", json={
        "repo_url": ""
    })
    # Should still accept (validation happens inside thread)
    assert response.status_code == 200


# ✅ TEST 5: Deploy with fake/invalid repo URL
def test_deploy_invalid_repo():
    response = client.post("/deploy", json={
        "repo_url": "https://github.com/fakeuserxyz/fakerepoxyz123"
    })
    assert response.status_code == 200
    assert "logs_url" in response.json()


# ✅ TEST 6: Deploy response contains logs URL
def test_deploy_response_has_logs_url():
    response = client.post("/deploy", json={
        "repo_url": "https://github.com/heroku/python-getting-started"
    })
    assert "logs_url" in response.json()


# ✅ TEST 7: Logs endpoint after deploy contains entries
def test_logs_not_empty_after_deploy():
    # Trigger a deploy first
    client.post("/deploy", json={
        "repo_url": "https://github.com/heroku/python-getting-started"
    })
    import time
    time.sleep(2)  # wait for thread to start

    response = client.get("/logs")
    assert response.status_code == 200
    logs = response.json()["logs"]
    assert len(logs) > 0


# ✅ TEST 8: Deploy missing field returns 422
def test_deploy_missing_field():
    response = client.post("/deploy", json={})
    assert response.status_code == 422


# ✅ TEST 9: Deploy with wrong field name returns 422
def test_deploy_wrong_field():
    response = client.post("/deploy", json={
        "url": "https://github.com/heroku/python-getting-started"
    })
    assert response.status_code == 422


# ✅ TEST 10: Logs returns 200 always
def test_logs_always_200():
    response = client.get("/logs")
    assert response.status_code == 200