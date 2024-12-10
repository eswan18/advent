from .framentable_filesystem import FragmentableFilesystem


def a(input: str) -> str:
    fs = FragmentableFilesystem.from_string(input)
    while success := fs.shift_last():
        ...
    return str(fs.checksum())