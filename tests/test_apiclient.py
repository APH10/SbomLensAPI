import os, pytest
from apiclient import APIClient
def test_require_key():
    with pytest.raises(ValueError): APIClient(api_key=None)
def test_auth_cache(tmp_path):
    tf=str(tmp_path/'tok'); c=APIClient(api_key='KEY', token_file=tf); c.token='x'; open(tf,'w').write('x'); c._load_token_if_valid(); assert c.token=='x'
