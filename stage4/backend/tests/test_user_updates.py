
from datetime import datetime

import pytest
from db import get_engine_db
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestUserUpdate:
    """Test users updates functionalities
    """
    access_token: str = ""
    user_id: str = ""
    old_username = "anthony"
    old_password = "anthony123456"

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
        request.cls.register(
            self=request.cls, username=request.cls.old_username,
            password=request.cls.old_password)
        response = client.post("/auth/login", data={
            "username": request.cls.old_username,
            "password": request.cls.old_password,
        })
        assert response.status_code == 200
        request.cls.access_token = response.json()['access_token']

    def update_user(self, do_auth=True, username=None, first_name=None,
                    last_name=None, password=None, json=None):
        """Call the patch update a user route from the API
        """
        if json is None:
            json = {}
        headers = {}
        if do_auth:
            headers = {"Authorization": f"Bearer {self.access_token}"}
        body = {}
        if username is not None:
            body['username'] = username
        if first_name is not None:
            body['first_name'] = first_name
        if last_name is not None:
            body['last_name'] = last_name
        if password is not None:
            body['password'] = password
        response = client.patch(
            "/users", headers=headers, json={**body, **json})
        if do_auth:
            assert response.status_code != 401
        return response

    def test_update_for_non_authintacted_users(self):
        """Test updating a username without authentication
        """
        assert self.access_token != ""
        response = self.update_user(do_auth=False)
        assert response.status_code == 401

    def test_update_without_any_data(self):
        """Test updating a user without giving any arugments
        """
        response = self.update_user()
        assert response.status_code == 200

    def test_update_username(self):
        """Test updates to the username
        """
        # check that updates dont happen if the data is invalid
        me = self.get_current_user()
        old_user = me.json()
        response = self.update_user(username="")
        assert response.status_code == 422
        new_user = me.json()
        print(old_user)
        print(new_user)
        assert old_user['username'] == self.old_username
        assert datetime.fromisoformat(
            new_user['updated_at']) == datetime.fromisoformat(
            old_user['updated_at'])

        # check that the data update if it is valid
        response = self.update_user(username="rakan")
        assert response.status_code == 200
        me = self.get_current_user()
        new_user = me.json()
        assert new_user['username'] == "rakan"
        assert datetime.fromisoformat(
            new_user['updated_at']) > datetime.fromisoformat(
            old_user['updated_at'])

    def test_update_first_name(self):
        """Test updating the first name
        """
        # check that updates dont happen if the data is invalid
        me = self.get_current_user()
        old_user = me.json()
        response = self.update_user(first_name="")
        assert response.status_code == 422
        new_user = me.json()

        # check that the data update if it is valid
        assert datetime.fromisoformat(
            new_user['updated_at']) == datetime.fromisoformat(
            old_user['updated_at'])
        response = self.update_user(first_name="Anthony")
        assert response.status_code == 200
        me = self.get_current_user()
        new_user = me.json()
        assert new_user['first_name'] == "Anthony"
        assert datetime.fromisoformat(
            new_user['updated_at']) > datetime.fromisoformat(
            old_user['updated_at'])

    def test_update_last_name(self):
        """Test updating the last name
        """
        # check that updates dont happen if the data is invalid
        me = self.get_current_user()
        old_user = me.json()
        response = self.update_user(last_name="")
        assert response.status_code == 422
        new_user = me.json()

        # check that the data update if it is valid
        assert datetime.fromisoformat(
            new_user['updated_at']) == datetime.fromisoformat(
            old_user['updated_at'])
        response = self.update_user(last_name="Killer")
        assert response.status_code == 200
        me = self.get_current_user()
        new_user = me.json()
        assert new_user['last_name'] == "Killer"
        assert datetime.fromisoformat(
            new_user['updated_at']) > datetime.fromisoformat(
            old_user['updated_at'])

    def test_update_password(self):
        """Test updating the password
        """
        # check that updates dont happen if the data is invalid
        me = self.get_current_user()
        old_user = me.json()
        response = self.update_user(password="")
        assert response.status_code == 422
        new_user = me.json()

        # check that the data update if it is valid
        assert datetime.fromisoformat(
            new_user['updated_at']) == datetime.fromisoformat(
            old_user['updated_at'])
        # check the user still can login with his old password
        response = client.post("/auth/login", data={
            "username": new_user['username'],
            "password": self.old_password
        })

        assert response.status_code == 200
        response = self.update_user(password="an12345678")
        assert response.status_code == 200
        me = self.get_current_user()
        new_user = me.json()
        assert datetime.fromisoformat(
            new_user['updated_at']) > datetime.fromisoformat(
            old_user['updated_at'])
        # check the user cant login with his old password
        response = client.post("/auth/login", data={
            "username": new_user['username'],
            "password": self.old_password
        })
        assert response.status_code != 200
        # check the user can login with his new password
        response = client.post("/auth/login", data={
            "username": new_user['username'],
            "password": "an12345678"
        })
        assert response.status_code == 200

    def test_update_with_random_fields(self):
        """Check random field names are not accepted
        """
        for field in ["askljfdhklsajdfjlkash", "", "12394e8hhkfa92834"]:
            response = self.update_user(json={
                field: "fklhfkhskf"
            })
            print(field)
            assert response.status_code == 422

    def test_update_username_to_an_already_exist_username(self):
        """Check that you cant update username to an already existent username
        """
        assert self.register(
            username="jhon", email="jhon@jjj.com").status_code == 200
        assert self.update_user(username="jhon").status_code == 422
