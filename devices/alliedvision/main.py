import argparse


from sipyco import pc_rpc, common_args
from driver import Camera


def get_argparser():
    parser = argparse.ArgumentParser(
        description="ARTIQ controller for the Alliedvision cameras"
    )
    parser.add_argument(
        "-d", "--device", required=True, default=None, help="Camera device ID"
    )

    common_args.simple_network_args(parser, 3255)
    common_args.verbosity_args(parser)

    return parser


def main():
    args = get_argparser().parse_args()

    camera = Camera(args.device)

    try:
        camera.start_streaming()

        pc_rpc.simple_server_loop(
            camera, common_args.bind_address_from_args(args), args.port
        )
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop_streaming()


if __name__ == "__main__":
    main()
