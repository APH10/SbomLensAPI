import pytest

from apiclient.client import APIClient


def test_require_key():
    with pytest.raises(ValueError):
        APIClient(api_key=None)


def test_auth_cache(tmp_path):
    tf = str(tmp_path / "tok")
    c = APIClient(api_key="KEY", token_file=tf)
    c._save_tokens(access_token="X", refresh_token="Y")
    access, refresh = c._load_token()
    assert access == "X"
    assert refresh == "Y"
