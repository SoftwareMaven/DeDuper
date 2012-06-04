import os
import os.path

import smhasher

BLOCKSIZE = 4096 * 1024 # 4k blocks for reading

class FileWrapper:
    seed = 11223344

    def __init__(self, dirpath, fname):
        self.dirpath = dirpath
        self.fname = fname
        s = os.stat(os.path.sep.join((dirpath, fname)))
        self.size = s.st_size
        self.modtime = s.st_mtime
        self.hash = None

    def __eq__(self, o):
        if self.size == o.size:
            if self.fname == o.fname and self.modtime == o.modtime:
                return True
            else:
                if not self.hash:
                    self._genhash()
                if not o.hash:
                    o._genhash()
                return self.hash == o.hash
        else:
            return False

    def __ne__(self, o):
        return not self.__eq__(o)

    __hash__ = object.__hash__

    def _genhash(self):
        hash_ = 0
        blocks = 0
        with open(os.path.sep.join((self.dirpath, self.fname)), 'rb') as f:
            data = f.read(BLOCKSIZE)
            while data:
                next_hash = smhasher.murmur3_x86_128(data, FileWrapper.seed)
                hash_ ^= (next_hash << blocks)
                data = f.read(BLOCKSIZE)
        self.hash = hash_
