import logging
from functools import wraps
from kalmoize.constants import DEFAULT_TIMEOUT
from kalmoize.constants import MEMCACHE_NONE
from kalmoize.utils import get
from kalmoize.utils import put


log = logging.getLogger(__name__)

def memoize(key_function, vkey_function=None, timeout=DEFAULT_TIMEOUT,
            allow_none=False, l1=True, use_deepcopy=True, optionaladd=False):
    """
    Decorator is caching result of functions and stores it in memcaches under provided key

      :key_function: functions that transforms args and kwargs to key. No cachonig if it returns None
      :vkey_function: version key function, it allows to invalidate many keys
      :l1: local cache per request
      :use_deepcopy: ---
      :timeout: maximal timeout
      :optionaladd: - store in cache only if it does not exists (for race conditions)
      :MEMOIZE_REFRESH: - enforces storing data into cache
    """
    def decorator(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            add_to_cache = optionaladd

            # 1. Creation of keys
            key = key_function
            vkey = vkey_function
            time_out = timeout

            # if MEMOIZE_REFRESH is provided, there is no reading, only forcing value save
            refresh = False
            if kwargs.has_key('MEMOIZE_REFRESH'):
                add_to_cache = False
                refresh = kwargs['MEMOIZE_REFRESH']
                del kwargs['MEMOIZE_REFRESH']

            if callable(key_function):
                key = key_function(*args, **kwargs)

            if key is not None:
                if callable(vkey_function):
                    vkey = vkey_function(*args, **kwargs)

                if callable(timeout):
                    time_out = timeout()

                log.debug("KEY %s", key)

                if not refresh:
                    # 2. Get data and return
                    result = get(key, l1, use_deepcopy=use_deepcopy)
                    if result is not None or result == MEMCACHE_NONE:
                        if result == MEMCACHE_NONE:
                            return
                        log.debug("Z CACHE")
                        return result

            # 3. Generating new data
            result = f(*args, **kwargs)

            if not allow_none and result is None:
                return

            if key is not None:
                put(key, result, time_out, vkey, l1, add_to_cache)

            return result
        return _wrapper
    return decorator