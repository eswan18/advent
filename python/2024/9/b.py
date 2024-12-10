from .filesystem import Filesystem

def b(input: str) -> str:
    fs = Filesystem.from_string(input)
    file_id = len(fs.files) - 1
    while file_id > 0:
        print(f'Shifting ID {file_id}')
        fs.shift_by_id(file_id)
        file_id -= 1
    return str(fs.checksum())