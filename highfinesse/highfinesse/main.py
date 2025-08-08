import argparse
import time
import json
from sipyco.pc_rpc import simple_server_loop
from sipyco import common_args
from .driver import Wavemeter


def add_common_args(parser):
    parser.add_argument(
        "--host",
        required=True,
        help="Connection string (e.g. '192.168.178.212', 'bc.example.com')",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Interval in seconds to report wavelength",
    )


def get_argparser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparser_pressure = subparsers.add_parser("pressure")
    add_common_args(subparser_pressure)

    subparser_temperature = subparsers.add_parser("temperature")
    add_common_args(subparser_temperature)

    subparser_frequency = subparsers.add_parser("frequency")
    add_common_args(subparser_frequency)

    subparser_wavelength = subparsers.add_parser("wavelength")
    add_common_args(subparser_wavelength)

    subparser_stream = subparsers.add_parser("stream")
    add_common_args(subparser_stream)

    subparser_sipyco = subparsers.add_parser("sipyco")
    common_args.simple_network_args(subparser_sipyco, 3249)
    common_args.verbosity_args(subparser_sipyco)
    add_common_args(subparser_sipyco)

    return parser


def main():
    args = get_argparser().parse_args()

    wm = Wavemeter(address=args.host)

    try:
        wm.open()

        if args.command == "pressure":
            while True:
                print(f"{wm.pressure()} mbar")
                time.sleep(args.interval)
        if args.command == "temperature":
            while True:
                print(f"{wm.temperature()} °C")
                time.sleep(args.interval)
        if args.command == "wavelength":
            while True:
                print(f"{wm.wavelength()} nm")
                time.sleep(args.interval)
        if args.command == "frequency":
            while True:
                print(f"{wm.frequency()} THz")
                time.sleep(args.interval)

        if args.command == "stream":
            wm.listen()

            def print_callback(param):
                print(json.dumps(param))

            wm.subscribe(print_callback)

            input("")

            wm.unlisten()
            wm.unsubscribe(print_callback)

        if args.command == "sipyco":
            common_args.init_logger_from_args(args)
            simple_server_loop(
                {"frequency_counter": fc},
                common_args.bind_address_from_args(args),
                args.port,
            )
    finally:
        wm.close()


if __name__ == "__main__":
    main()
