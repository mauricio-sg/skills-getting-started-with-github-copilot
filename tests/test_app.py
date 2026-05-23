import pytest


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_activity_list(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "Chess Club" in body
    assert "Programming Class" in body


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "new_student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}

    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert email in participants


def test_signup_for_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_from_activity_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Participant successfully removed"}

    get_response = client.get("/activities")
    participants = get_response.json()[activity]["participants"]
    assert email not in participants


@pytest.mark.parametrize(
    "activity,email,expected_detail",
    [
        ("Nonexistent Activity", "student@mergington.edu", "Activity not found"),
        ("Chess Club", "missing@mergington.edu", "Participant not found"),
    ],
)
def test_unregister_nonexistent_activity_or_participant_returns_404(client, activity, email, expected_detail):
    # Arrange

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == expected_detail
