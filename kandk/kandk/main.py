import argparse
from sipyco.pc_rpc import simple_server_loop
from sipyco import common_args
from .driver import FrequencyCounter

def add_common_args(parser):
    parser.add_argument(
        '--host',
        required=True,
        help="Connection string (e.g. '192.168.178.212', 'HOST:abc.example.com')"
    )
    parser.add_argument(
        '--channels',
        type=int,
        default=8,
        help="Number of channels to enable on the device (default: 8)"
    )


def get_argparser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparser_stream = subparsers.add_parser("stream")
    add_common_args(subparser_stream)

    subparser_sipyco = subparsers.add_parser("sipyco")
    common_args.simple_network_args(subparser_sipyco, 3249)
    common_args.verbosity_args(subparser_sipyco)
    add_common_args(subparser_sipyco)

    return parser

def main():
    args = get_argparser().parse_args()

    try:
        fc = FrequencyCounter(
            connection=args.host,
         channels=args.channels
        )

        if args.command == "stream":
            while True:
                freqs = fc.report()
                if freqs is not None:
                    print(", ".join(f"{f:.6f}" for f in freqs))

        if args.command == "sipyco":
            common_args.init_logger_from_args(args)
            simple_server_loop(
                {"frequency_counter": fc},
                common_args.bind_address_from_args(args),
                args.port,
            )
    finally:
        fc.close()

if __name__ == '__main__':
    main()
