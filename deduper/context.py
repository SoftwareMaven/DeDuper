import os

from . import wrapper

class DuplicatesContext:
    '''
    Keeps track of information about which files are duplicates and which are not.
    '''

    def __init__(self, find_suspected=False):
        self.find_suspected = find_suspected
        self.files = {}
        self.duplicates = {}

    def process_path(self, path, depth=-1, progress=None, ignore_re_list=[]):
        '''
        Checks the given path for duplicates.

        Parameters:
          path: the path to process
          progress: a callable that takes two parameters: a string and an integer.
                    It will be called each time a new directory is entered with the
                    path. The integer is the number of duplicates found.
          depth: The depth of subdirectories that should be processed. -1 means "all of them"
                 (depth is not implemented yet)
        '''
        for dirpath, dirnames, filenames in os.walk(path):


    @classmethod
    def store(cls, context, path=None):
        '''
        Stores the context for future use
        '''

    @classmethod
    def load(cls, path=None):
        '''
        Loads a previously stored context
        '''
