import argparse

MAX_BYTE = 1024


def base_parser(with_address: bool):
    parser = argparse.ArgumentParser()
    if with_address:
        parser.add_argument('host', type=str, action='store')
    parser.add_argument('port', type=int, action='store')
    return parser
