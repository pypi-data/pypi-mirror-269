from discovery_connect import Client, Config
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Upload file(s) to discovery")
    parser.add_argument('-w', '--workbook_uuid', required=True, type=str, help="UUID of the target workbook.")
    parser.add_argument('-f', '--file', required=False, type=str, help="Path to a single file to be uploaded.")
    parser.add_argument('-a', '--acquisition_name', required=False, type=str, help="Name for the zip archive for the files.")
    parser.add_argument('-F', '--files', nargs='*', help="List of file names.")

    parser.add_argument('-l', '--login', required=True, type=str, help="Discovery login")
    parser.add_argument('-p', '--password', required=True, type=str, help="Discovery password")
    parser.add_argument('-u', '--url', required=True, type=str, help="Discovery URL")
    parser.add_argument('-k', '--client_key', required=True, type=str, help="Discovery client API key")
    parser.add_argument('-s', '--client_secret', required=True, type=str, help="Discovery client API secret")

    args = parser.parse_args()

    return args, parser

def main():
    args, parser = parse_args()

    configuration = Config(HOST=args.url,
                            USERNAME=args.login,
                            PASSWORD=args.password,
                            CLIENT_ID=args.client_key,
                            CLIENT_SECRET=args.client_secret)
    client = Client(config=configuration)

    if args.file:
        client.upload_file(args.file, args.workbook_uuid)
    elif args.acquisition_name and args.files:
        client.upload_files(args.files, args.acquisition_name, args.workbook_uuid)
    else :
       parser.print_help()

if __name__ == "__main__":
    main()

