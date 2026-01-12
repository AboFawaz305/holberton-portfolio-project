import pytest
from db import get_engine_db
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestOrganizations:
    """ test class for Organizations"""

    @pytest.fixture(autouse=True)
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
            }
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
        self.register()
        rs = self.register()
        assert rs.status_code == 422
        assert rs.json()["detail"] == "Organization already added"
