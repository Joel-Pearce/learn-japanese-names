import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_home(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_learn_dashboard(client, user, flashcard):
    url = reverse("learn")
    response = client.get(url)
    assert response.status_code == 302

    client.login(username="example_user", password="Abc123!!!")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context.get("flashcard") == flashcard

    response = client.post(url, {"user_response": "Incorrect answer"})
    assert (
        response.context.get("message")
        == "I'm afraid that is incorrect. Please try again."
    )

    response = client.post(url, {"user_response": "にち"})
    assert response.status_code == 302


@pytest.mark.django_db
def test_review_dashboard(client, user, flashcard, deck, review):
    url = reverse("review")
    response = client.get(url)
    assert response.status_code == 302

    client.login(username="example_user", password="Abc123!!!")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context.get("flashcard") == review

    response = client.post(url, {"user_response": "Incorrect answer"})
    assert (
        response.context.get("message")
        == "I'm afraid that is incorrect. Please try again."
    )

    response = client.post(url, {"user_response": "にち"})
    assert response.status_code == 302
