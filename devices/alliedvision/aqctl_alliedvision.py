#!/usr/bin/env python3

import argparse
import asyncio

from sipyco.pc_rpc import simple_server_loop
from sipyco.common_args import simple_network_args, init_logger_from_args


def get_argparser():
    parser = argparse.ArgumentParser(
        description="ARTIQ controller for the Alliedvision cameras"
    )
    parser.add_argument("-d", "--device", default=None, help="Camera device ID")
    simple_network_args(parser, 3254)

    return parser


def main():
    args = get_argparser().parse_args()
    init_logger_from_args(args)


if __name__ == "__main__":
    main()
