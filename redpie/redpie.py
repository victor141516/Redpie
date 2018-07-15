# -*- coding: utf-8 -*-
import pickle
import redis


def checkpickle(func):
    def w(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pickle.UnpicklingError:
            print('You are using a Redis database used by other than Redpie. You may want to stop doing this.')
            return 'You are using a Redis database used by other than Redpie. You may want to stop doing this.'
    return w


class Redpie(dict):
    def __init__(self, db=0, host='localhost', port=6379):
        super(Redpie, self).__init__()
        self._db = db
        self._host = host
        self._port = port
        self._redis = redis.StrictRedis(host=host, port=port, db=db)

    @checkpickle
    def __setitem__(self, k, v):
        self._redis.set(k, pickle.dumps(v))

    @checkpickle
    def __getitem__(self, k):
        v = self._redis.get(k)
        if v is None:
            raise KeyError(k)
        return pickle.loads(v)

    @checkpickle
    def __contains__(self, k):
        return self._redis.exists(k)

    @checkpickle
    def __delitem__(self, k):
        if not self._redis.exists(k):
            raise KeyError(k)
        self._redis.delete(k)
        return None

    @checkpickle
    def __eq__(self, o):
        return True

    @checkpickle
    def __format__(self, spec=None):
        obj = {}
        for key in self._redis.scan_iter():
            obj[key.decode("utf-8")] = pickle.loads(self._redis.get(key))
        return format(obj, spec)

    @checkpickle
    def __iter__(self):
        for key in self._redis.scan_iter():
            yield key.decode('utf-8')

    @checkpickle
    def __len__(self):
        return self._redis.dbsize()

    def __new__(cls, *args, **kwargs):
        return super(Redpie, cls).__new__(cls)

    def __reduce__(self):
        raise NotImplementedError

    @checkpickle
    def __repr__(self):
        obj = {}
        for key in self._redis.scan_iter():
            obj[key.decode("utf-8")] = pickle.loads(self._redis.get(key))
        return obj.__repr__()

    @checkpickle
    def clear(self):
        self._redis.flushdb()

    @checkpickle
    def copy(self):
        print("I don't know how to implement this ¯\_(ツ)_/¯")
        raise NotImplementedError

    @checkpickle
    def fromkeys(self, keys, value=None):
        print("I don't know how to implement this ¯\_(ツ)_/¯")
        raise NotImplementedError

        # new_r = Redpie()
        # new_r._redis.flushdb()
        # for key in keys:
        #     new_r._redis.set(key, pickle.dumps(value))
        # return new_r

    @checkpickle
    def get(self, key, default_value=None):
        v = self._redis.get(key)
        if v is None:
            return default_value
        else:
            return pickle.loads(v)

    @checkpickle
    def items(self):
        obj = {}
        for key in self._redis.scan_iter():
            obj[key.decode("utf-8")] = pickle.loads(self._redis.get(key))
        return obj.items()

    @checkpickle
    def keys(self):
        keys = self._redis.keys()
        keys = [k.decode('utf-8') for k in keys]
        return dict.fromkeys(keys).keys()

    @checkpickle
    def pop(self, k):
        if not self._redis.exists(k):
            raise KeyError(k)
        v = self._redis.get(k)
        self._redis.delete(k)
        return pickle.loads(v)

    @checkpickle
    def popitem(self):
        k = self._redis.randomkey()
        if k is None:
            raise KeyError('popitem(): empty')
        v = self._redis.get(k)
        self._redis.delete(k)
        return (k.decode('utf-8'), pickle.loads(v))

    @checkpickle
    def setdefault(self, k, dv=None):
        v = self._redis.get(k)
        if v is None:
            self._redis.set(k, pickle.dumps(dv))
            return dv
        else:
            return pickle.loads(v)

    @checkpickle
    def update(self, n):
        for k in n.keys():
            self._redis.set(k, pickle.dumps(n[k]))

    @checkpickle
    def values(self):
        keys = self._redis.keys()
        obj = {}
        for k in keys:
            obj[k.decode('utf-8')] = pickle.loads(self._redis.get(k))
        return obj.values()
