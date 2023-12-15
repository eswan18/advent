from .platform import Platform


def a(input: str) -> str:
    platform = Platform.build_from_str(input)
    platform.tilt('North')
    load = platform.load()
    return str(load)
