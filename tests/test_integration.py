import pytest

from apiclient.client import APIClient

API_KEY = "TESTKEY"
USER = "user"
PASS = "pass"


@pytest.mark.integration
def test_flow(api_base_url, tmp_path):
    c = APIClient(base_url=api_base_url, api_key=API_KEY, token_file=f"{tmp_path}/.token")
    # Check connection with server
    response = c.check_status()
    assert len(response) > 0
    assert response["data"]["status"] == "OK"
    # Authenticate user
    t = c.authenticate(USER, PASS)
    assert len(t) > 0
    assert t["data"]["access_token"] == "dummytoken"
    # Retrieve data
    response = c.api_get("end1")
    assert response["data"]["data"] == "hello"
    # Send a file
    f = tmp_path / "t.json"
    f.write_text("{}")
    r = c.api_post_file("load", {"project": "p", "release": "0.1"}, "file", str(f))
    assert r["data"]["filename"] == "t.json"
    # Logout
    c.reset_auth()
    # Demonstrate status still works
    response = c.check_status()
    assert len(response) > 0
    assert response["data"]["status"] == "OK"
    # But get unauthorised reposnse if not authenticated
    response = c.api_get("end1")
    assert response["status_code"] == 403