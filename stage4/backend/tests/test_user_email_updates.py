import pytest
from db import get_engine_db
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestUserEmailsUpdate:
    """Test user emails updates functionalities
    """
    access_token: str = ""

    def register(self, first_name="ali", last_name="redmon", username="ali",
                 email="ali@gmail.com", password="ali12345"):
        """Register a user for testing
        """
        return client.post("/auth/register", json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "username": username
        })

    def get_current_user(self):
        """get the current user information from the api
        """
        return client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {self.access_token}"})

    @pytest.fixture(scope="class", autouse=True)
    def setup_assure_empty_database(self, request):
        """Assure the database is empty before testing the registeration
            and create a user for testing
        """
        db = get_engine_db()
        db.users.delete_many({})
        request.cls.register(self=request.cls)
        response = client.post("/auth/login", data={
            "username": "ali",
            "password": "ali12345"
        })
        assert response.status_code == 200
        request.cls.access_token = response.json()['access_token']

    def test_add_email_without_giving_an_email(self):
        """add email without any argument
        """
        response = client.post("/users/emails", headers={
            "Authorization": f"Bearer {self.access_token}"
        })
        assert response.status_code == 422

    def test_add_email(self):
        """add a valid email
        """
        response = client.post("/users/emails", headers={
            "Authorization": f"Bearer {self.access_token}"
        },
            json={
            "email": "ali2@gmail.com"
        })
        assert response.status_code == 200

        nu = self.get_current_user().json()
        assert len(nu['email']) == 2
        assert "ali2@gmail.com" in nu["email"]

    def test_add_non_unique_email(self):
        """fail if add a non unique email
        """
        response = client.post("/users/emails", headers={
            "Authorization": f"Bearer {self.access_token}"
        },
            json={
            "email": "ali3@gmail.com"
        })
        assert response.status_code == 200

        response = client.post("/users/emails", headers={
            "Authorization": f"Bearer {self.access_token}"
        },
            json={
            "email": "ali3@gmail.com"
        })
        assert response.status_code == 422

    def test_delete_email(self):
        """delete an email
        """
        old_me = self.get_current_user().json()
        assert len(old_me["email"]) == 3
        assert "ali2@gmail.com" in old_me["email"]
        response = client.delete("/users/emails/1", headers={
            "Authorization": f"Bearer {self.access_token}"

        })
        assert response.status_code == 200
        me = self.get_current_user().json()
        assert len(me["email"]) == 2
        assert "ali2@gmail.com" not in me["email"]
