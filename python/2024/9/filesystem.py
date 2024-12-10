from dataclasses import dataclass
from typing import Iterator

@dataclass
class File:
    id: int
    at: int
    length: int

    @property
    def end(self) -> int:
        '''Get the position of the last occupied byte'''
        return self.at + self.length - 1
    
    def checksum(self) -> int:
        checksum = 0
        at = self.at
        while at <= self.end:
            checksum += self.id * at
            at += 1
        return checksum

@dataclass
class Filesystem:
    files: list[File] # All the files, in order.

    @classmethod
    def from_string(cls, s: str):
        files = []
        at = 0
        # Every other position is a file; the remaining are free space.
        is_file = True
        id = 0
        for c in s.strip():
            size = int(c)
            if is_file:
                files.append(File(id=id, at=at, length=size))
                id += 1
            at += size
            is_file = not is_file
        return cls(files=files)
    
    @staticmethod
    def find_first_open(files: list[File]) -> int:
        '''Given an ordered list of files, find the first open space.'''
        at = 0
        files_to_search = files
        while len(files_to_search) > 0:
            if at < files_to_search[0].at:
                return at
            # Skip to the end of the first file.
            at = files_to_search[0].end + 1
            # Remove the first file from our files to consider.
            files_to_search = files_to_search[1:]
        return files[-1].end + 1
    
    def open_blocks(self) -> Iterator[tuple[int, int]]:
        at = 0
        files_to_search = self.files
        while len(files_to_search) > 0:
            if at < files_to_search[0].at:
                # Use all the space up until the next file.
                open_space = files_to_search[0].at - at
                yield (at, open_space)
            # Skip to the end of the first file.
            at = files_to_search[0].end + 1
            # Remove the first file from our files to consider.
            files_to_search = files_to_search[1:]
        return
    
    def shift_by_id(self, id: int):
        '''Take the bytes with the given ID and try to find an earlier place for them.'''
        files = [
            (index, file) for (index, file) in enumerate(self.files)
            if file.id == id
        ]
        if len(files) > 1:
            raise RuntimeError('multiple files with same ID')
        index, file = files[0]
        for (at, length) in self.open_blocks():
            if length >= file.length and at < file.at:
                # We found a new home for this file!
                self.files.pop(index)
                file.at = at
                for i, existing_file in enumerate(self.files):
                    if existing_file.at > at:
                        self.files.insert(i, file)
                        return
    
    def __str__(self) -> str:
        s = ''
        at = 0
        files_to_search = self.files
        while len(files_to_search) > 0:
            while at < files_to_search[0].at:
                s += '.'
                at += 1
            # Write the next file.
            id = files_to_search[0].id
            while at <= files_to_search[0].end:
                s += str(id)
                at += 1
            # Remove the first file from our files to consider.
            files_to_search = files_to_search[1:]
        final_at = self.files[-1].end + 1
        while at < final_at:
            s += '.'
            at += 1
        return s

    def checksum(self) -> int:
        running_sum = 0
        for file in self.files:
            running_sum += file.checksum()
        return running_sum