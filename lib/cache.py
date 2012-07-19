# -*- coding: utf-8 -*-

import functools
import cachecore

class cachedrequest(object):
    """Decorator. Caches the return value of a Web request in the filesystem.
    """

    def __init__(self, cache_dir, default_timeout):
        self.cache = cachecore.FileSystemCache(
            cache_dir=cache_dir, default_timeout=default_timeout)


    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            if len(args) > 0:
                cid = str(args[0])
                result = self.cache.get(cid)
                if result: return result
            result = fn(*args)
            if len(args) > 0:
                self.cache.set(cid, result)
            return result
        return decorated


    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)
