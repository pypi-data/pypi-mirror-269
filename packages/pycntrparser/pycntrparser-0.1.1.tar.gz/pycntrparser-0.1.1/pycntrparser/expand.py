def expand(path):
    paths = [path]
    if path.is_dir():
        paths = filter(exclude, path.glob("**/*.txt"))
    return paths


def exclude(path):
    return path.stem != "README"
