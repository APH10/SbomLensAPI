# Copyright (C) 2025 APH10
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import logging
import os

from apiclient.client import APIClient
from apiclient.version import VERSION


def make_client(args):
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception:
        pass
    base_url = args.base_url or os.getenv("API_BASE_URL")
    api_key = args.api_key or os.getenv("API_KEY")
    return APIClient(base_url=base_url, api_key=api_key, debug=args.debug)


def _format_response(response, output_file):
    logging.debug(f"Response code: {response.get('status_code')}")
    if response.get("data") is not None:
        if output_file is None:
            print(json.dumps(response.get("data"), indent=2))
        else:
            with open(str(output_file), "w", encoding="utf-8") as f:
                f.write(str(response.get("data")).replace("'", '"'))


def cmd_status(args):
    client = make_client(args)
    # print(json.dumps(client.check_status(), indent=2))
    _format_response(client.check_status(), args.output)


def cmd_auth(args):
    client = make_client(args)
    token = client.authenticate(args.username, args.password)
    _format_response({"token": token}, args.output)


def cmd_get(args):
    client = make_client(args)
    _format_response(client.api_get(args.endpoint), args.output)


def cmd_post(args):
    client = make_client(args)
    if args.file:
        fields = {}
        for it in args.field or []:
            k, v = it.split("=", 1)
            fields[k] = v
        file_field, path = args.file.split("=", 1)
        _format_response(
            client.api_post_file(args.endpoint, fields, file_field, path), args.output
        )
    else:
        payload = json.loads(args.data) if args.data else {}
        _format_response(client.api_post(args.endpoint, payload), args.output)


def cmd_logout(args):
    client = make_client(args)
    client.reset_auth()
    print("Token removed")


def main():

    app_name = "sbomlenscli"
    parser = argparse.ArgumentParser(
        prog=app_name,
        description="A CLI utility to interact with the SBOMLens platform",
        epilog="For support send email to support@aph10.com",
    )

    parser.add_argument("--base-url", help="specify the URL of the SBOMLens platform")
    parser.add_argument(
        "--api-key", help="specify API Key to use the SBOMLens platform"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="show debug information",
    )
    parser.add_argument(
        "--output",
        action="store",
        default=None,
        help="output filename (default: output to stdout)",
    )
    parser.add_argument("-V", "--version", action="version", version=VERSION)

    subparser = parser.add_subparsers(dest="cmd", required=True)

    status_command = subparser.add_parser("status")
    status_command.set_defaults(func=cmd_status)

    auth_command = subparser.add_parser("auth")
    auth_command.add_argument("username")
    auth_command.add_argument("password")
    auth_command.set_defaults(func=cmd_auth)

    get_command = subparser.add_parser("get")
    get_command.add_argument("endpoint")
    get_command.add_argument("--data")
    get_command.set_defaults(func=cmd_get)

    post_command = subparser.add_parser("post")
    post_command.add_argument("endpoint")
    post_command.add_argument("--data")
    post_command.add_argument("--field", action="append")
    post_command.add_argument("--file")
    post_command.set_defaults(func=cmd_post)

    logout_command = subparser.add_parser("logout")
    logout_command.set_defaults(func=cmd_logout)

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    try:
        args.func(args)
    except Exception as e:
        logging.debug(f"{e}")
        print("[ERROR] Unable to perform request")


if __name__ == "__main__":
    main()
