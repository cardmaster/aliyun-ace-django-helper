from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache
from alibaba import cache
from django.utils import six

class AliOCSCache(BaseCache):
    def __init__(self, name, params):
        super(AliOCSCache, self).__init__(params)

        if isinstance(name, six.string_types):
            self._aliname = name
        else:
            self._aliname = None
        self._options = params.get('OPTIONS', None)

        if self._options:
            self._backend = cache.Cache(self._options)
        elif self._aliname:
            self._backend = cache.Cache(self._aliname)
        else:
            self._backend = cache.Cache()
    def _keytr(self, key, version):
        newkey = str(self.make_key(key, version = version))
        self.validate_key(newkey)
        return newkey

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        self._backend.add(self._keytr(key, version), value, timeout)

    def get(self, key, default=None, version=None, acquire_lock=True):
        return self._backend.get(self._keytr(key, version))

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        return self._backend.set(self._keytr(key, version), value, timeout)

    def incr(self, key, delta=1, version=None):
        return self._backend.incr(self._keytr(key, version), delta)

    def delete(self, key, version=None):
        return self._backend.delete(self._keytr(key, version))

    def clear(self):
        self._backend.init_cache()

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        safe_data = {}
        for key, value in data.items():
            key = self._keytr(key, version)
            safe_data[key] = value
        self._backend.set_multi(safe_data, timeout)

    def get_many(self, keys, timeout=DEFAULT_TIMEOUT, version=None):
        new_keys = [self._keytr(x, version) for x in keys]
        ret = self._backend.get_multi(new_keys)
        if ret:
            _ = {}
            m = dict(zip(new_keys, keys))
            for k, v in ret.items():
                _[m[k]] = v
            ret = _
        return ret

