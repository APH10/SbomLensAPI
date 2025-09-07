import json, os, logging, requests
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url=None, api_key=None, token_file=None, debug=False):
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except Exception:
            pass
        self.base_url = (base_url or os.getenv('SBOMLENS_API_BASE_URL','http://127.0.0.1:5000/api/v1')).rstrip('/')
        self.api_key = api_key or os.getenv('SBOMLENS_API_KEY')
        if not self.api_key:
            raise ValueError('API key is required')
        self.session = requests.Session()
        self.session.headers.update({'X-API-Key': self.api_key})
        self.token_file = Path(token_file) if token_file else Path.home() / ".sbomlens_token"
        self.token_max_age_days = int(os.getenv("SBOMLENS_TOKEN_MAX_AGE_DAYS", 30))
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self.token, self.refresh_token = self._load_token()

    # Helper functions

    def _load_token(self):
        if not self.token_file.exists():
            return None, None
        if datetime.now() - datetime.fromtimestamp(self.token_file.stat().st_mtime) > timedelta(days=self.token_max_age_days):
            logger.info("Stored token expired, re-authentication required")
            return None, None
        # return self.token_file.read_text().strip()
        try:
            data = json.loads(self.token_file.read_text())
            return data.get("access_token"), data.get("refresh_token")
        except Exception:
            return None, None        
        

    def _save_tokens(self, access_token, refresh_token):
        # self.token_file.write_text(token)
        # self.token = token
        token_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        self.token_file.write_text(json.dumps(token_data))
        self.token = access_token
        self.refresh_token = refresh_token

    # def _headers(self):
    #     h = {'X-API-Key': self.api_key}
    #     if self.token:
    #         h['Authorization'] = f'Bearer {self.token}'
    #     return h

    def _headers(self, include_auth=True):
        headers = {"x-api-key": self.api_key}
        if include_auth and self.token:
            headers["Authorization"] = f"Bearer {str(self.token)}"
        return headers

    def _handle_response(self, response):
        try:
            data = response.json()
        except ValueError:
            data = response.text
        if response.ok:
            return {"success": True, "status_code": response.status_code, "data": data}
        else:
            logger.error(f"API error {response.status_code}: {data}")
            return {"success": False, "status_code": response.status_code, "error": data}

    def _refresh_access_token(self):
        """Attempt to refresh the access token using refresh token."""
        if not self.refresh_token:
            return False
        url = f"{self.base_url}/refresh"
        headers = {"Authorization": f"Bearer {self.refresh_token}", "x-api-key": self.api_key}
        resp = self.session.post(url, json={"refresh_token": self.refresh_token}, headers=headers)
        result = self._handle_response(resp)
        if result["success"] and "access_token" in result["data"]:
            logger.info("Access token refreshed")
            self._save_tokens(result["data"]["access_token"], self.refresh_token)
            return True
        logger.warning("Failed to refresh access token")
        return False

    def _request_with_refresh(self, method, url, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update(self._headers())
        response = self.session.request(method, url, headers=headers, **kwargs)
        logger.debug(f"Response {response.status_code} Text {response.text}")
        if response.status_code == 401 and "expired" in response.text.lower():
            logger.info("Access token expired, refreshing...")
            if self._refresh_access_token():
                headers.update(self._headers())  # new access token
                response = self.session.request(method, url, headers=headers, **kwargs)
        return self._handle_response(response)


    # PUBLIC API

    def reset_auth(self):
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
        self.token, self.refresh_token = None, None
        logger.info("Tokens reset")


    def check_status(self):
        url = f"{self.base_url}/status"
        #response = requests.get(url, headers=self._headers(include_auth=False))
        response = self.session.get(url, headers=self._headers(include_auth=False))
        return self._handle_response(response)
        # r = self.session.get(f"{self.base_url}/status", headers=self._headers())
        # r.raise_for_status()
        # return r.json()

    def authenticate(self, username, password):
        url = f"{self.base_url}/auth"
        payload = {"username": username, "password": password}
        response = self.session.post(url, json=payload, headers=self._headers(include_auth=False))
        result = self._handle_response(response)
        # if result["success"] and "access_token" in result["data"]:
        #     self._save_token(result["data"]["access_token"])
        #     return result["data"]["access_token"]
        if result["success"]:
            tokens = result["data"]
            if "access_token" in tokens and "refresh_token" in tokens:
                self._save_tokens(tokens["access_token"], tokens["refresh_token"])
        return result
        # r = self.session.post(f"{self.base_url}/auth", headers=self._headers(), json={'username':username,'password':password})
        # r.raise_for_status()
        # token = r.json().get('access_token')
        # if not token:
        #     raise RuntimeError('No token returned')
        # with open(self.token_file,'w') as f:
        #     f.write(token)
        # self.token = token
        # return token

    def api_get(self, endpoint):
        # if not self.token:
        #     raise RuntimeError('Authenticate first')
        url = f"{self.base_url}/{endpoint}"
        # resp = self.session.get(url, headers=self._headers())
        # return self._handle_response(resp)
        return self._request_with_refresh("GET", url)
        # r = self.session.get(f"{self.base_url}/{endpoint.lstrip('/')}", headers=self._headers())
        # r.raise_for_status()
        # return r.json()

    def api_post(self, endpoint, data):
        # if not self.token:
        #     raise RuntimeError('Authenticate first')
        url = f"{self.base_url}/{endpoint}"
        # resp = self.session.post(url, json=data, headers=self._headers())
        # return self._handle_response(resp)
        return self._request_with_refresh("POST", url, json=data)
        # r = self.session.post(f"{self.base_url}/{endpoint.lstrip('/')}", headers=self._headers(), json=data or {})
        # r.raise_for_status()
        # return r.json()

    def api_post_file(self, endpoint, fields, file_field, file_path):
        if not self.token:
            raise RuntimeError('Authenticate first')
        url = f"{self.base_url}/{endpoint}"
        files = {file_field: open(file_path, "rb")}
        try:
            # resp = self.session.post(url, data=fields, files=files, headers=self._headers())
            return self._request_with_refresh("POST", url, data=fields, files=files)
        finally:
            files[file_field].close()
        return {"success": False, "status_code": 401, "error": {}}
        # return self._handle_response(resp)
        # with open(file_path,'rb') as fh:
        #     files = {file_field: fh}
        #     r = self.session.post(f"{self.base_url}/{endpoint.lstrip('/')}", headers=self._headers(), data=fields or {}, files=files)
        #     r.raise_for_status()
        #     return r.json()
