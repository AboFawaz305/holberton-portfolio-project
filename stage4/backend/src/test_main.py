"""Unit tests to test the API
"""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from main import app, get_engine_db

SECRET_KEY = "wow_secret_KEY"
ALGORITHM = "HS256"

client = TestClient(app)


def test_always_pass():
    """Make sure the testing suite work"""
    assert True


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
            "/register",
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
            "/register",
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
        return client.post("/login", data={"username": username,
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
        """testing for user info return for route /me"""
        data = self.login(username="ali", password="ali12345")
        token = data.json()["access_token"]

        response = client.get("/me",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200

        body = response.json()
        assert body["username"] == "ali"
        assert body["first_name"] == "ali"
        assert body["last_name"] == "redmon"
        assert body["email"][0] == "ali@gmail.com"

    def test_sending_invalid_token(self):
        """testing sending invalid token to route /me"""
        data = self.login(username="ali", password="ali12345")
        token = data.json()["access_token"]
        response = client.get(
            "/me", headers={"Authorization": f"Bearer {token + 'SS'}"}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "invalid token"


class TestOrganizations:
    """ test class for Organizations"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_assure_empty_database(self):
        """Assure the database is empty before testing the registeration"""
        db = get_engine_db()
        db.organizations.delete_many({})

    def register(
        self, organization_name="BIG_ORG", email_domain="@GG.EDU",
        location="RIYADH"
    ):
        """Make an org registeration request"""
        return client.post(
            "/organizations",
            data={
                "organization_name": organization_name,
                "email_domain": email_domain,
                "location": location,
            },
        )

    def test_empty_org_registeration(self):
        """empty input test"""
        assert self.register(organization_name="").status_code == 422
        assert self.register(email_domain="").status_code == 422
        assert self.register(location="").status_code == 422

    def test_wrong_input_org_registeration(self):
        """empty wrong input test"""
        assert self.register(organization_name="2").status_code == 422
        assert self.register(email_domain="2").status_code == 422
        assert self.register(location="2").status_code == 422

    def test_valid_data_returned_by_id(self):
        """testing valid data returned by id"""
        org = self.register()
        assert org.status_code == 200

        org_id = org.json()["organization_id"]

        rs = client.get(f"/organizations/{org_id}")
        body = rs.json()

        assert rs.status_code == 200
        assert body["organization_id"] == org_id
        assert body["organization_name"] == "BIG_ORG"
        assert body["email_domain"] == "@GG.EDU"
        assert body["location"] == "RIYADH"

    def test_registeratoin_of_a_repetitive_org(self):
        """Test uniqueness validation of orgs"""
        rs = self.register()
        assert rs.status_code == 422
        assert rs.json()["detail"] == "Organization already added"


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
        return client.post("/register", json={
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
            "/me", headers={"Authorization": f"Bearer {self.access_token}"})

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
        response = client.post("/login", data={
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
        response = client.post("/login", data={
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
        response = client.post("/login", data={
            "username": new_user['username'],
            "password": self.old_password
        })
        assert response.status_code != 200
        # check the user can login with his new password
        response = client.post("/login", data={
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
