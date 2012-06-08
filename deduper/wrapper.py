import os
import os.path

import smhasher

from .decorators import reify

BIG_BLOCKSIZE = 16 * 1024 # 16k blocks for the full hash
SMALL_BLOCKSIZE = 4 * 1024 # 4k blocks for the first block hash

def get_wrapper_for_file(path):
    return GenericFileWrapper(path)

class GenericFileWrapper:
    seed = 11223344

    def __init__(self, path):
        self.path = path
        s = os.stat(self.path)
        self.size = s.st_size
        self.modtime = s.st_mtime

    def __str__(self):
        return self.path

    def __eq__(self, o):
        if self.size == o.size and self.first_block_hash == o.first_block_hash:
            return self.hash == o.hash
        else:
            return False

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__():
        return self.first_block_hash

    @reify
    def first_block_hash(self):
        with open(self.path, 'rb') as f:
            data = f.read(SMALL_BLOCKSIZE)
            return smhasher.murmur3_x86_128(data, GenericFileWrapper.seed)

    @reify
    def hash(self):
        """ The full hash of the file """
        hash_ = self.size
        blocks = 0
        with open(self.path, 'rb') as f:
            data = f.read(BIG_BLOCKSIZE)
            while data:
                next_hash = smhasher.murmur3_x86_128(data, GenericFileWrapper.seed)
                hash_ ^= (next_hash << blocks)
                data = f.read(BIG_BLOCKSIZE)
                blocks = blocks + 1 if blocks < 16 else 0
        return hash_
