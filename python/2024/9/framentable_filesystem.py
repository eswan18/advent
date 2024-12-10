from dataclasses import dataclass

@dataclass
class FragmentableFilesystem:
    bytes: list[int | None] # The IDs of files at each byte location, or None where there is no file.

    @classmethod
    def from_string(cls, s: str):
        bytes = []
        # Every other position is a file; the remaining are free space.
        is_file = True
        id = 0
        for c in s.strip():
            size = int(c)
            if is_file:
                bytes.extend([id] * size)
                id += 1
            else:
                bytes.extend([None] * size)
            is_file = not is_file
        fs = cls(bytes=bytes)
        fs.trim()
        return fs
    
    def trim(self):
        '''Remove all trailing empty bytes.'''
        n_to_remove = 0
        for b in reversed(self.bytes):
            if b is not None:
                break
            n_to_remove += 1
        if n_to_remove == 0:
            return
        self.bytes = self.bytes[:-n_to_remove]
    
    def first_open_block(self) -> int:
        return self.bytes.index(None)
    
    def shift_last(self) -> bool:
        '''
        Take the last byte and try to find an earlier place for it.
        
        Returns True on success, False if there is nowhere to move the byte.
        '''
        b = self.bytes[-1]
        if b is None:
            raise RuntimeError("untrimmed bytes")
        try:
            insert_at = self.first_open_block()
        except ValueError:
            return False
        else:
            self.bytes[insert_at] = self.bytes.pop()
            self.trim()
            return True
    
    def __str__(self) -> str:
        s = ''
        for b in self.bytes:
            if b is None:
                s += '.'
            else:
                s += str(b)
        return s
    
    def checksum(self) -> int:
        running_sum = 0
        for i, b in enumerate(self.bytes):
            running_sum += i * b
        return running_sum