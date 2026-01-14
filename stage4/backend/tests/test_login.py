
import pytest
from db import get_engine_db
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestLogin:
    """login unit tests definitions"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_assure_empty_database(self):
        """Assure the database is empty before testing the registeration"""
        db = get_engine_db()
        db.users.delete_many({})
        self.register()

    def register(
        self,
        first_name="ali",
        last_name="redmon",
        username="ali",
        email="ali@gmail.com",
        password="ali12345",
    ):
        """Make a registeration request"""
        return client.post(
            "/auth/register",
            json={
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
            },
        )

    def login(self, username="ali", password="ali12345"):
        """make loging request"""
        return client.post("/auth/login", data={"username": username,
                           "password": password})

    def test_empty_login(self):
        """empty input test"""
        assert self.login(username="").status_code == 422
        assert self.login(password="").status_code == 422

    def test_invalid_login_info(self):
        """wrong input test"""
        assert self.login(username="allll").status_code == 401
        assert self.login(password="12344444").status_code == 401

    def test_valid_login_info(self):
        """valid input test"""
        data = self.login(username="ali", password="ali12345")
        assert data.status_code == 200

    def test_geting_user_info(self):
        """testing for user info return for route /auth/me"""
        data = self.login(username="ali", password="ali12345")
        token = data.json()["access_token"]

        response = client.get("/auth/me",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200

        body = response.json()
        assert body["username"] == "ali"
        assert body["first_name"] == "ali"
        assert body["last_name"] == "redmon"
        assert body["email"][0] == {'is_verified': False,
                                    'value': 'ali@gmail.com'}

    def test_sending_invalid_token(self):
        """testing sending invalid token to route /auth/me"""
        data = self.login(username="ali", password="ali12345")
        token = data.json()["access_token"]
        response = client.get(
            "/auth/me", headers={"Authorization": f"Bearer {token + 'SS'}"}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "invalid token"
