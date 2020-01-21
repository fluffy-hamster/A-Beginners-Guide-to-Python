def profile(function, *args, **kwargs):
    """ Returns performance statistics (as a string) for the given function.
    """
    def _run():
        function(*args, **kwargs)
    import cProfile as profile
    import pstats
    import os
    import sys; sys.modules['__main__'].__profile_run__ = _run
    id = function.__name__ + '()'
    profile.run('__profile_run__()', id)
    p = pstats.Stats(id)
    p.stream = open(id, 'w')
    p.sort_stats('tottime').print_stats(20)
    p.stream.close()
    s = open(id).read()
    os.remove(id)
    return s