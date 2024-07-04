#!/usr/bin/env python3

import argparse
import asyncio

from sipyco import pc_rpc, common_args
from driver import Wavemeter


def get_argparser():
    parser = argparse.ArgumentParser(
        description="ARTIQ controller for HighFinesse wavelength meters"
    )
    parser.add_argument(
        "-a",
        "--address",
        required=True,
        default=None,
        help="Network address (host:port) used by the wavemeter http service running on the computer connected to the wavemeter.",
    )

    common_args.simple_network_args(parser, 3249)
    common_args.verbosity_args(parser)

    return parser


def main():
    args = get_argparser().parse_args()
    common_args.init_logger_from_args(args)

    loop = asyncio.get_event_loop()

    wavemeter = Wavemeter(args.address)

    try:
        pc_rpc.simple_server_loop(
            {"wavemeter": wavemeter},
            common_args.bind_address_from_args(args),
            args.port,
            loop=loop,
        )
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == "__main__":
    main()
