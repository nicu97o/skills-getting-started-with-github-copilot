import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    # Arrange
    # (No setup needed, uses in-memory data)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

# Test POST /activities/{activity_name}/signup

def test_signup_for_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Ensure clean state
    client.delete(f"/activities/{activity}/remove?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/remove?email={email}")

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    client.delete(f"/activities/{activity}/remove?email={email}")
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()
    # Clean up
    client.delete(f"/activities/{activity}/remove?email={email}")

# Test DELETE /activities/{activity_name}/remove

def test_remove_participant_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser3@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/remove?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

def test_remove_participant_not_found():
    # Arrange
    activity = "Chess Club"
    email = "nonexistent@mergington.edu"
    client.delete(f"/activities/{activity}/remove?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/remove?email={email}")

    # Assert
    assert response.status_code == 400
    assert "not found" in response.json()["detail"].lower()
