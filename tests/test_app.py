import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def reset_activities():
    # Reset the in-memory activities to their initial state for test isolation
    for activity in activities.values():
        if isinstance(activity, dict):
            if "participants" in activity:
                activity["participants"] = []

# --- GET /activities ---
def test_get_activities():
    # Arrange
    reset_activities()
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# --- POST /activities/{activity_name}/signup ---
def test_signup_success():
    # Arrange
    reset_activities()
    email = "test1@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]

def test_signup_duplicate():
    # Arrange
    reset_activities()
    email = "test2@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"

def test_signup_activity_not_found():
    # Arrange
    reset_activities()
    email = "test3@mergington.edu"
    # Act
    response = client.post(f"/activities/Nonexistent/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

# --- POST /activities/{activity_name}/unregister ---
def test_unregister_success():
    # Arrange
    reset_activities()
    email = "test4@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")
    # Act
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]

def test_unregister_not_registered():
    # Arrange
    reset_activities()
    email = "test5@mergington.edu"
    # Act
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"

def test_unregister_activity_not_found():
    # Arrange
    reset_activities()
    email = "test6@mergington.edu"
    # Act
    response = client.post(f"/activities/Nonexistent/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
