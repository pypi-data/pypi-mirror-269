MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

try:
    from tornado.options import options
    DEFAULT_TIMEOUT = options.CACHE_DEFAULT_TIMEOUT
except Exception:
    DEFAULT_TIMEOUT = 2 * DAY   

                                
MEMCACHE_NONE = '⪔Noneद⪣'        # Special value to have a distinction between  real None and miss

