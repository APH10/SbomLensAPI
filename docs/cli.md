CLI Reference (apicli)

The CLI provides convenient access to the SBOMLENS API via the apicli command.

## Global Options

--base-url URL – API base URL (default: http://127.0.0.1:5000/api/v1).
--api-key KEY – SBOMLENS API key (can also be set in .env).
--debug – enable verbose logging.

## Commands

status
- Check if the API is available.

```bash
apicli status
```

auth USERNAME PASSWORD
- Authenticate and store a token.

```bash
apicli auth user pass
```

get ENDPOINT
- Perform a GET request.

```bash
apicli get end1
```

post ENDPOINT [--data JSON | --field key=value | --file field=path]
- Perform a POST request.

--data – JSON string.
--field – key=value form field (can repeat).
--file – field=path for file upload.

Examples:

```bash
apicli post end2 --data '{"hello":"world"}'
apicli post load --field project=test --field release=0.1 --file file=/tmp/test.json
```

reset-auth
- Remove the stored token file.

```bash
apicli reset-auth
```

## Debugging

Use --debug to see request/response logs:

```bash
apicli --debug get end1CLI docs
```