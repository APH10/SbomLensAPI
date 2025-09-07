import argparse, json, os, logging
from dotenv import load_dotenv
from apiclient import APIClient

def make_client(args):
    load_dotenv()
    base_url = args.base_url or os.getenv('API_BASE_URL')
    api_key = args.api_key or os.getenv('API_KEY')
    return APIClient(base_url=base_url, api_key=api_key, debug=args.debug)

def cmd_status(args):
    client = make_client(args)
    print(json.dumps(client.check_status(), indent=2))

def cmd_auth(args):
    client = make_client(args)
    token = client.authenticate(args.username, args.password)
    print(json.dumps({'token':token}, indent=2))

def cmd_get(args):
    client = make_client(args)
    print(json.dumps(client.api_get(args.endpoint), indent=2))

    # payload = json.loads(args.data) if args.data else {}
    # print(json.dumps(client.api_get(args.endpoint, payload), indent=2))

def cmd_post(args):
    client = make_client(args)
    if args.file:
        fields={}
        for it in args.field or []:
            k,v = it.split('=',1)
            fields[k]=v
        file_field, path = args.file.split('=',1)
        print(json.dumps(client.api_post_file(args.endpoint, fields, file_field, path), indent=2))
    else:
        payload = json.loads(args.data) if args.data else {}
        print(json.dumps(client.api_post(args.endpoint, payload), indent=2))

def cmd_reset(args):
    client = make_client(args)
    client.reset_auth()
    print('Token removed')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--base-url')
    p.add_argument('--api-key')
    p.add_argument('--debug', action='store_true')

    sub=p.add_subparsers(dest='cmd', required=True)

    sp=sub.add_parser('status')
    sp.set_defaults(func=cmd_status)

    sp=sub.add_parser('auth')
    sp.add_argument('username')
    sp.add_argument('password')
    sp.set_defaults(func=cmd_auth)

    sp=sub.add_parser('get')
    sp.add_argument('endpoint')
    sp.add_argument('--data')
    sp.set_defaults(func=cmd_get)

    sp=sub.add_parser('post')
    sp.add_argument('endpoint')
    sp.add_argument('--data')
    sp.add_argument('--field', action='append')
    sp.add_argument('--file')
    sp.set_defaults(func=cmd_post)

    sp=sub.add_parser('reset-auth')
    sp.set_defaults(func=cmd_reset)

    args=p.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    args.func(args)

if __name__=='__main__':
    main()
