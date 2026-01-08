import pytest
from db import get_engine_db
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRegisteration:
    """Registeration unit tests definitions"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_assure_empty_database(self):
        """Assure the database is empty before testing the registeration"""
        db = get_engine_db()
        db.users.delete_many({})

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

    def test_registeration_with_empty_fields(self):
        """Test the failure of registeration if any of the fields is empty"""
        assert self.register(username="").status_code == 422
        assert self.register(email="").status_code == 422
        assert self.register(password="").status_code == 422

    def test_registeration_of_new_valid_account(self):
        """Test creating a valid user account"""
        res = self.register()
        assert res.status_code == 200

    def test_registeratoin_of_a_repetitive_accouunt(self):
        """Test uniqueness validation of users accounts"""
        assert self.register().status_code == 422
