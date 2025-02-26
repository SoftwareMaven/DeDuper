from . import context

def find_duplicates(paths, find_suspected=False, progress=None, ignore_re_list=[],
                    min_file_size=1024):
    """
    Finds duplicate files in the given paths. If find_suspected is True, use heuristics
    such as ID3 tags, to determine if files appear to be the same. progress is a callable
    that takes two parameters (string, int) that will be updated each time a new path
    is entered with that path and the number of duplicates found.

    Returns a deduper.context.DuplicatesContext
    """
    ctx = context.DuplicatesContext(find_suspected=find_suspected, min_file_size=min_file_size)
    for path in paths:
        ctx.process_path(path, progress=progress)
    return ctx


