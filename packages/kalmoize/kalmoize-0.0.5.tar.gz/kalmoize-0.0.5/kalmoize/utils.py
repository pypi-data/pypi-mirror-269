import sys

import logging
import random
from copy import deepcopy
from tornado.options import options
import memcache

from kalmoize.constants import MEMCACHE_NONE

log = logging.getLogger(__name__)

try:   
    PREFIX = options.CACHE_PREFIX
except Exception:
    PREFIX = ""


local_memoize_cache = {}
cache = memcache.Client(options.cache_server_list)

## Funkcje podstawowe
def gen_version():
    """Key version generator matching keys and vkeys
    :return: version number, random int
    :rtype: int
    """
    return random.randint(0, sys.maxsize)

def localcache_put(key, value):
    """Wklada dane do localcache.
    :param key: klucz pod którym zostaną zapamiętane dane
    :type key: str
    :param value: dane do zapamiętania
    """
    global local_memoize_cache
    local_memoize_cache[key] = value

def localcache_put_dict(values_dict):
    """puts dict to local cache.
    :param values_dict: dictionary to update
    :type key: dict
    """
    global local_memoize_cache
    local_memoize_cache.update(values_dict)

def localcache_get(key, use_deepcopy=True):
    """Get data from local cache
    :param key: data key
    :type key: str
    :return: saved data or  MEMCACHE_NONE if None was pushed
    """
    global local_memoize_cache

    if key not in local_memoize_cache:
        return

    if use_deepcopy:
        result = deepcopy(local_memoize_cache[key])
    else:
        result = local_memoize_cache[key]

    if isinstance(result, dict):
        if result.get('vkey') and result.get('version'):
            desired_version = localcache_get(result.get('vkey'), use_deepcopy=use_deepcopy)
            if desired_version != result['version']:
                return
        # return results
        return result

    log.debug("LGET %r=%r", key, result)

    # return results
    return result

def get(key, l1=True, use_deepcopy=True):
    """Gets data from provided key
    :param key: 
    :type key: str
    :param l1: use one request cache or not
    :type l1: bool
    :return: - data stored in cache or  MEMCACHE_NONE if None was put
    """
    global cache
    # get data from local cache
    if l1:
        result = localcache_get(key, use_deepcopy=use_deepcopy)
        if result:
            if isinstance(result, int):
                return
            elif result.get('vkey') and result.get('version'):
                desired_version = _get(result['vkey'], use_deepcopy=use_deepcopy)
                if desired_version != result['version']:
                    return
            return result['value']

    # get data from memcache
    result = cache.get(key)
    log.debug("FROM CACHE: %r", result)
    if not result:
        return

    # checking version
    if result.get('vkey') and result.get('version'):
        desired_version = _get(result['vkey'], False, use_deepcopy=use_deepcopy)
        if desired_version != result['version']:
            return

    # put to local cache and return results
    if l1:
        localcache_put(key, result)
        #local_memoize_cache[key] = result
    log.debug("GET %r=%r", key, result)
    return result['value']

def _put(key, value, timeout=0, l1=True, optionaladd=False):
    """Put data directly to cache.
    :param key: key.
    :type key: str
    :param value: data to put
    :param timeout: timeout in seconds
    :type timeout: int
    :param l1: use l1
    :type l1: bool
    """
    #global local_memoize_cache
    global cache
    if value is None:
        value = MEMCACHE_NONE
    log.debug("_PUT %r=%r", key, value)

    # opcjonalne dodanie elementu do cache tylko wtedy jesli go jeszcze nie ma
    if optionaladd:
        resp = cache.add(key, value, timeout)
    else:
        resp = cache.set(key, value, timeout)

    if l1:
        localcache_put(key, deepcopy(value))
        #local_memoize_cache[key] = deepcopy(value)
    return resp

def _get(key, l1=True, use_deepcopy=True):
    """get data from cache or localcache.
    :param key: key
    :type key: str
    :param l1: check l1 or not
    :type l1: bool
    """
    #global local_memoize_cache
    global cache
    # gt data from localcache
    if l1:
        result = localcache_get(key, use_deepcopy=use_deepcopy)
        if result:
            return result

    # get data from memcache
    result = cache.get(key)
    log.debug("_GET %r=%r", key, result)
    if not result:
        return

    # put to local cache
    if l1:
        localcache_put(key, result)
        #local_memoize_cache[key] = result
    return result


def _get_many(keys, l1=True, use_deepcopy=True):
    """get data from cache or localcache.
    :param keys: list of keys
    :type key: str
    :param l1: use 1 request cache or not
    :type l1: bool
    """
    results = {}
    global cache
    # get data from local cache
    if l1:
        for key in keys:
            result = localcache_get(key, use_deepcopy=use_deepcopy)
            if result:
                results[key] = result

    # get data from memcache
    cache_results = cache.get_multi([k for k in keys if k not in results])
    if cache_results:
        # put to local cache and return results
        if l1:
            localcache_put_dict(cache_results)

        results.update(cache_results)

    return results


def put(key, value, timeout=0, vkey=None, l1=True, optionaladd=False):
    """Put data to cache
    :param key: key
    :type key: str
    :param value: data to put
    :param l1: whether to use one request cache or not
    :type l1: bool
    :param timeout: timeout in seconds
    :type timeout: int
    :param optionaladd: set is optional, for race conditions
    """
    #global local_memoize_cache
    global cache
    log.debug("PUT %r=%r", key,value)
    value_dict = dict(value=None, vkey=None, version=None)
    value_dict['vkey'] = vkey

    if value is None:
        value = MEMCACHE_NONE

    if vkey:
        # creating vkey version
        current_version = _get(vkey, l1)
        if not current_version:
            current_version = gen_version()
            _put(vkey, current_version, timeout, l1, optionaladd)
        value_dict['version'] = current_version

    value_dict['value'] = value
    log.debug("PUT %r = dict: %r", key, value_dict)

    # adding to cache
    if optionaladd:
        resp = cache.add(key, value_dict, timeout)
    else:
        resp = cache.set(key, value_dict, timeout)

    if l1:
        localcache_put(key, deepcopy(value_dict))
        #local_memoize_cache[key] = deepcopy(value_dict)
    return resp


def get_many(keys, l1=True, use_deepcopy=True):
    """Get data fom given keys from l1 and memcache.
    :param keys: keys
    :type key: str list
    :param l1: use l1 cache)
    :type l1: bool
    :return: - returns data or MEMOIZE_NONE when it is None
    """
    results = {}
    l1_vkeys = set()
    l1_vkeys_results = {}

    # get data from l1
    if l1:
        l1_results = {}

        for key in keys:
            result = localcache_get(key, use_deepcopy=use_deepcopy)
            if result:
                # We do always put dict in put method
                # we ensure whether it is not int
                if isinstance(result, int):
                    continue

                l1_results[key] = result

        # getting keys
        l1_vkeys = set([v.get('vkey') for v in l1_results.itervalues() if v.get('vkey') and v.get('version')])
        l1_vkeys_results = _get_many(l1_vkeys, use_deepcopy=use_deepcopy)

        # checking version for local data
        for (k, v) in l1_results.iteritems():
            if v.get('version') and v.get('vkey'):
                if v.get('version') != l1_vkeys_results.get(v.get('vkey')):
                    continue
            results[k] = v

    # get data from memcache, that are not available in l1 cache
    cache_results = cache.get_multi([k for k in keys if k not in results])
    if cache_results:
        # getting version keys
        cache_vkeys = set([v.get('vkey') for v in cache_results.itervalues() if v.get('vkey') and
                                                                                v.get('version') and
                                                                                v.get('vkey') not in l1_vkeys])
        cache_vkeys_results = _get_many(cache_vkeys, False, use_deepcopy=use_deepcopy)
        cache_vkeys_results.update(l1_vkeys_results)

        # checking whether version is correct
        valid_cache_results = {}
        for (k, v) in cache_results.iteritems():
            if v.get('version') and v.get('vkey'):
                if v.get('version') != cache_vkeys_results.get(v.get('vkey')):
                    continue
            valid_cache_results[k] = v

        if l1:
            localcache_put_dict(valid_cache_results)

        results.update(valid_cache_results)

    # delete version data from results
    final_dict = {}
    for (k, v) in results.iteritems():
        final_dict[k] = v['value'] if v is not None else None

    return final_dict


def delete(*keys):
    """invalidate many keys
    :param keys: list of keys
    """
    return invalidate(*keys)

def invalidatev(*keys, **kwargs):
    """Invalidate version keys and set new version
    """
    global local_memoize_cache
    resps = []
    for key in keys:
        v = gen_version()
        resps.append( cache.set(key, v) )
        localcache_put(key, v)
        local_memoize_cache[key] = v
    return resps

def invalidate(*keys, **kwargs):
    """invalidate data.
    :param keys: list of keys
    """
    global local_memoize_cache

    resps = []
    for key in keys:
        resps.append( cache.delete(key) )
        if key in local_memoize_cache:
            del local_memoize_cache[key]
    return resps

def localcache_clear():
    """clears local cache, run it after first request"""
    global local_memoize_cache
    local_memoize_cache = {}