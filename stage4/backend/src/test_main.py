"""Unit tests to test the API
"""
import pytest
from appwrite.services.users import Users
from fastapi.testclient import TestClient

from main import app, get_client

client = TestClient(app)


def test_always_pass():
    """Make sure the testing suite work
        """
    assert True


class TestRegisteration:
    """Registeration unit tests definitions
    """
    @pytest.fixture(scope="class", autouse=True)
    def setup_assure_empty_database(self):
        """Assure the database is empty before testing the registeration
        """
        us = Users(get_client())
        all_users = us.list()["users"]
        for u in all_users:
            us.delete(user_id=u["$id"])

    def register(self, name="ali redmon", email="ali@gmail.com",
                 password="ali12345"):
        """Make a registeration request
        """
        return client.post("/register", json={
            "email": email,
            "password": password,
            "name": name,
        })

    def test_registeration_with_empty_fields(self):
        """Test the failure of registeration if any of the fields is empty
        """
        assert self.register(name="").status_code == 422
        assert self.register(email="").status_code == 422
        assert self.register(password="").status_code == 422

    def test_registeration_of_new_valid_account(self):
        """Test creating a valid user account
        """
        res = self.register()
        assert res.status_code == 200

    def test_registeratoin_of_a_repetitive_accouunt(self):
        """Test uniqueness validation of users accounts
        """
        assert self.register().status_code == 422
