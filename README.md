# SBOMLENS CLI

A Python API client library (`apiclient`) and CLI (`sbomlenscli`) for interacting with the SBOMLENS REST API. The API requires a valid API key and supports token-based authentication.

## Features
- Status platform check
- Token authentication with caching and timed expiry
- File upload via POST
- Configurable API base URL
- API key required for all requests
- CLI (`sbomlenscli`) for convenience
- Logging/debug mode

## Installation

Clone the repo and install dependencies using the following command:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

For development, use
```bash
pip install -e .
```

The tool requires Python 3 (3.9+). It is recommended to use a virtual python environment especially
if you are using different versions of python. `virtualenv` is a tool for setting up virtual python environments which
allows you to have all the dependencies for the tool set up.

## Configuration

Copy .env.example and edit as needed:

```bash
cp .env.example .env
```

```bash
SBOMLENS_API_KEY – required
SBOMLENS_API_BASE_URL – default: http://127.0.0.1
SBOMLENS_TOKEN_MAX_AGE_DAYS – default: 30
```

## Usage

```bash
usage: sbomlenscli [-h] [--base-url BASE_URL] [--api-key API_KEY] [--debug] [--output OUTPUT] [-V] {status,auth,get,post,logout} ...

A CLI utility to interact with the SBOMLens platform

positional arguments:
  {status,auth,get,post,logout}

options:
  -h, --help            show this help message and exit
  --base-url BASE_URL   specify the URL of the SBOMLens platform
  --api-key API_KEY     specify API Key to use the SBOMLens platform
  --debug               show debug information
  --output OUTPUT       output filename (default: output to stdout)
  -V, --version         show program's version number and exit

For support send email to support@aph10.com
```

## Quick Start

The following exmaples assume that the environment variables have been set. If not, add '--apikey xxxxx' to each command to specify the API key and ''--base-ul yyyyy' to specify the platform address.

### Check System Status

This command should be used to confirm that the SBOMLens platform is available. 

```bash
sbomlenscli status
```

A typical response is:

```
{
  "status": "ok",
  "timestamp": "22 Sep 2025 18:20:42",
  "version": "0.1.8",
  "uptime": "0 days 01 hours 38 minutes 05 seconds"
}

```

If the platform is not available or accessible, an error will be returned.

```
[ERROR] Unable to perform request
```

### Authentication

Before any interaction with the SBOMLens platform, a valid user needs to authenticate with the platform. If a user is already authenticated with the platform, this request to autenticate 

Once authenticated, a token is stored on the system for a period of up to 30 days (the )

```bash
sbomlenscli auth username password
```

If the username and password are valid, the client will be logged in.

If the username and/or password are not valid, the foloowing error will be returned

```bash
ERROR:apiclient.client:API error 401: {'message': 'Bad username or password'}
```

### Retrieve Data

The general formatof a request to retrieve data is 

```bash
sbomlenscli get <endpoint>

```

The following endpoints are supported

| Endpoint | Parameter | Description   |
| --------- |---------|----------|
| sbom    | None     | Returns an index of all of the available SBOMs. Unique identifier (SBOM id) of each SBOM is provided. |
| sbom/<id>     | SBOM id   | Returns details of the specified SBOM.  |
| sbom/vuln/<id>     | SBOM id     | Returns the set of vulnerabilities for the specified SBOM. |
| application     | None    | Returns an index of all of the available applications. Unique identifier (App id) of each application is provided.|
| application/vuln/<id>     | App id     | Returns the set of vulnerabilities for the specified application. |
| asset    | None    | Returns an index of all of the available assets. Unique identifier (Asset id) of each asset is provided. |
| asset/vuln/<id>     | Asset id    | Returns the set of vulnerabilities for the specified application.    |
| system     | None    | Returns the system configuration identifying the assets, applications and SBOMs.    |
| system/vuln     | None    | Returns the set of vulnerabilities for the system. |
| vulnerability/<id>     | Vulnerability Id    | Returns deatils of the specified vulnerability.    |
| component | None    | Returns a summary of all of the components within the system.   |
| component/<id> | Component Name    | Returns a list of vulnerable components matching the component name. |



### Upload a file

The following command is used to upload a SBOM into the system

```bash
sbomlenscli post load --field project="Test Project" --field release="0.1" --file sbomfile=/tmp/test.json
```

The project, release and sbomfile parameters must be specified.

Various errors can be returned e.g. if the file cannot be found, the project and release has already been defined.

After the request has been acknowledged, there will be a delay whilst the SBOM is processed before details of the SBOM (e.g, vulnerabilities) can be accessed

###  Logout

```bash
sbomlenscli logout
```

This will logout the currently authenticated user.

## Licence

Licenced under the Apache 2.0 Licence.

## Feedback and Contributions

Bugs and feature requests can be made via GitHub Issues.