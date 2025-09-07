APIClient Library Documentation

The APIClient class provides programmatic access to the SBOMLENNS REST API requiring an API key and token-based authentication.

## Configuration

The client can be configured via environment variables or parameters:

SBOMLENS_API_KEY (required) – included in all requests.
SBOMLENS_API_BASE_URL (default: http://127.0.0.1:5000/api/v1).
SBOMLENS_TOKEN_MAX_AGE_DAYS (default: 30).

Authentication tokens are cached in a file (default: ~/.sbomlens_token) and reused if valid.

## Initialisation

```python
from apiclient import APIClient
client = APIClient(base_url="http://127.0.0.1:5000/api/v1", api_key="TESTKEY", debug=True)
```

## Methods

check_status()
- Check if the API is available.

```python
print(client.check_status())
# → {"status": "OK"}
```python

authenticate(username, password)
- Authenticate and store the returned token.

```python
token = client.authenticate("user", "pass")
print(token)
```python

api_get(endpoint)
- Send a GET request with authentication.

```python
data = client.api_get("end1")
print(data)
```

api_post(endpoint, data)
- Send a POST request with JSON data.

```python
resp = client.api_post("end2", {"key": "value"})
print(resp)
```python

api_post_file(endpoint, fields, file_field, file_path)
- Send a multipart POST with fields and a file.

```python
resp = client.api_post_file("load", {"project":"test","release":"0.1"}, "file", "/tmp/test.json")
print(resp)
```

reset_auth()
- Remove the stored token, forcing re-authentication.

```python
client.reset_auth()
```

## Example Workflow

```python
client = APIClient(api_key="TESTKEY")
# Check service is available
status = client.check_status()
if status.get("status", "Fail") == "ok":
    # System available
    client.authenticate("user", "pass")
    # Get data...
    print(client.api_get("end1"))
    # Add file
    client.api_post_file("load", {"project":"test"}, "file", "data.json")
```