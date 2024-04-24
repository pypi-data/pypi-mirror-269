from trackingmore.classes.api import TrackingMore

from configparser import ConfigParser
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()

    parser.add_argument('tracking_number', nargs="?", help='Tracking number to track')
    parser.add_argument('--carrier', '-c', help='Carrier to track (carrier code – see --list-carriers/-l, auto-detected if not specified)')
    parser.add_argument('--detect-carrier', '-d', action='store_true', help='Detect and output carrier from tracking number')
    parser.add_argument('--list-carriers', '-l', action='store_true', help='List carriers')
    parser.add_argument('--key', '-k', help='TrackingMore API Key (overrides config)')
    parser.add_argument('--config-file', '-f', help='Config file (default: settings.ini in working directory)', default='settings.ini')

    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config_file)

    if (args.tracking_number or args.carrier) and args.list_carriers:
        print("Cannot specify both tracking number and --list-carriers/-l")
        exit(1)

    api_key = args.key or config['TrackingMore']['APIKey']

    api = TrackingMore(api_key)

    if args.list_carriers:
        for carrier in api.get_carriers():
            print(f"{carrier['courier_name']} ({carrier['courier_code']})")

    elif args.tracking_number:
        if args.detect_carrier:
            for carrier in api.detect_carrier(args.tracking_number):
                print(f"{carrier['courier_name']} ({carrier['courier_code']})")

        else:
            print(api.track_shipment(args.tracking_number, args.carrier))

    else:
        print("No tracking number specified - use --help for usage")

if __name__ == '__main__':
    main()