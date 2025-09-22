import pytest

from apiclient.client import APIClient

API_KEY = "TESTKEY"
USER = "user"
PASS = "pass"


@pytest.mark.integration
def test_flow(api_base_url, tmp_path):
    c = APIClient(base_url=api_base_url, api_key=API_KEY)
    assert c.check_status()["status"] == "OK"
    t = c.authenticate(USER, PASS)
    assert t
    assert c.api_get("end1")["data"] == "hello"
    f = tmp_path / "t.json"
    f.write_text("{}")
    r = c.api_post_file("load", {"project": "p", "release": "0.1"}, "file", str(f))
    assert r["filename"] == "t.json"
