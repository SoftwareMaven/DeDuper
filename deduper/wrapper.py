import os
import os.path

import smhasher

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.ogg import OggFileType


from .decorators import reify

BIG_BLOCKSIZE = 16 * 1024 # 16k blocks for the full hash
SMALL_BLOCKSIZE = 4 * 1024 # 4k blocks for the first block hash

def _data_from_mp3(path):
    tag = MP3(path, ID3=EasyID3)
    return tag['artist'][0], tag['album'][0], tag['title'][0], tag.info.bitrate, int(tag.info.length)

def _data_from_mp4(path):
    tag = MP4(path)
    return tag['\xa9ART'][0], tag['\xa9alb'][0], tag['\xa9nam'][0], tag.info.bitrate, int(tag.info.length)


AUDIO_HANDLERS = { 'mp3': _data_from_mp3,
                   'm4a': _data_from_mp4,
                   'mp4': _data_from_mp4,
                   'm4b': _data_from_mp4,
                   'm4p': _data_from_mp4,
                   'm4v': _data_from_mp4,
                   }

def get_wrapper_for_file(path):
    wrapper = None
    extension = path.split('.')[-1]
    if extension in AUDIO_HANDLERS:
        try:
            wrapper = AudioWrapper(path, handler=AUDIO_HANDLERS[extension])
        except Exception:
            import traceback; traceback.print_exc()
    if not wrapper:
        wrapper = GenericFileWrapper(path)
    return wrapper

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

class AudioWrapper(GenericFileWrapper):
    def __init__(self, path, handler=None):
        self.path = path
        tag_info = handler(path)
        self.artist, self.album, self.title, self.bitrate, self.length = tag_info
        self.size = self.bitrate
        hash_info = ':'.join((self.artist, self.album, self.title,
                              unicode(self.bitrate), unicode(self.length)))
        self.hash = self.first_block_hash = hash(hash_info)
