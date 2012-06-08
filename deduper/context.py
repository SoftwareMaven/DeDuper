import os

from .wrapper import get_wrapper_for_file

# The default list of directory names to ignore. For safety, these cannot be overridden
# In addition to these, we will automatically ignore any path that starts with a '.'
IGNORE_DIRS = [
    ]

class DuplicatesContext:
    '''
    Keeps track of information about which files are duplicates and which are not.
    '''

    def __init__(self, find_suspected=False, min_file_size=0):
        self.find_suspected = find_suspected
        self.min_file_size = min_file_size
        self.files = {}
        self.visited = set()
        self.duplicates = []
        self.dups = 0

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
            progress and progress(dirpath, self.dups)
            # If we modify dirnames here, we won't traverse them later
            for dirname in dirnames:
                if dirname.startswith('.') or dirname in IGNORE_DIRS:
                    dirnames.remove(dirname)
            for fname in filenames:
                if fname.startswith('.'):
                    continue
                try:
                    file_path = os.path.realpath(os.path.sep.join((dirpath, fname)))
                    wrapper = self._create_wrapper(file_path)
                    if wrapper is None:
                        continue
                    files = self.files.setdefault(wrapper.first_block_hash, [])
                    for test_wrapper in files:
                        if wrapper == test_wrapper:
                            if wrapper.path == test_wrapper.path:
                                raise Exception("Paths are the same: {} / {}".
                                                format(wrapper.path, test_wrapper.path))
                            self.duplicates.append((test_wrapper, wrapper,))
                            self.dups+=1
                            break
                    else:
                        files.append(wrapper)
                except (OSError, IOError) as e:
                    # Problem opening file. It is likely a symlink that doesn't have
                    # a destination or some other oddity like trying to open a socket
                    continue

    def _create_wrapper(self, file_path):
        '''
        Creates a FileWrapper for the given path. This may return <code>None</code> if
        we don't want this wrapper processed (for instance, it has already been processed).
        '''
        if file_path in self.visited:
            return None
        self.visited.add(file_path)
        wrapper = get_wrapper_for_file(file_path)
        if wrapper.size < self.min_file_size:
            return None
        return wrapper


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
