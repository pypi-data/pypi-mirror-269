from argparse import ArgumentParser
from pathlib import Path


def parse():
    parser = ArgumentParser()
    parser.add_argument("path", nargs="+", type=Path)
    return parser.parse_args()
