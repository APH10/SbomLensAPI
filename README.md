# SBOMLENS API Client Project

Reusable Python API client library (`apiclient`) and CLI (`apicli`) for interacting with the SBOMLENS REST API that requires an API key and token-based authentication.

## Features
- Status check (`/status`)
- Token authentication with caching & expiry
- File upload via POST (`/load`)
- Configurable API base URL
- API key required for all requests
- CLI (`apicli`) for convenience
- Logging/debug mode

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

For development:
```bash
pip install -e .
```

## Configuration

Copy .env.example and edit as needed:

```bash
cp .env.example .env
```

SBOMLENS_API_KEY – required
SBOMLENS_API_BASE_URL – default: http://127.0.0.1:5000/api/v1
SBOMLENS_TOKEN_MAX_AGE_DAYS – default: 30

## Quick Start

### Check System Status

```bash
apicli status
```

### Authenticate:

```bash
apicli auth user pass
```

### Retrieve Data

```bash
apicli auth end1
```

### Upload a file

```bash
apicli post load --field project=test --field release=0.1 --file file=/tmp/test.json
```

###  Reset token

```bash
apicli reset-auth
```

## Documentation

Library Reference
CLI Reference

## License

Apache 2.0