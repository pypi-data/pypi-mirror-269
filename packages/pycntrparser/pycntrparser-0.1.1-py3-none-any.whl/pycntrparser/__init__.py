from multiprocessing import Pool
from itertools import chain
from .args.parse import parse as parse_args
from .expand import expand
from .parse import parse


def main():
    args = parse_args()
    paths = args.path
    filepaths = set(chain.from_iterable(map(expand, paths)))
    with Pool() as pool:
        pool.map(parse, filepaths)
