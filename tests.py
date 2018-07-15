import pytest
from redpie import Redpie


@pytest.fixture
def r():
    r = Redpie(10)
    r.clear()
    return r


def test_all(r):
    r['qwe'] = 2
    assert r['qwe'] is 2
    assert 'qwe' in r
    assert 'q' not in r
    del(r['qwe'])
    with pytest.raises(KeyError):
        del(r['qwe'])
    r['qwe'] = 2
    assert format(r) == "{'qwe': 2}"
    i = iter(r)
    assert next(i) == 'qwe'
    with pytest.raises(StopIteration):
        next(i)
    assert len(r) is 1
    r['www'] = 3
    assert len(r) is 2
    del(r['www'])
    r.__reduce__()
    assert r.__repr__() == "{'qwe': 2}"
    assert r._redis.dbsize() > 0
    r.clear()
    assert r._redis.dbsize() is 0
    r['qwe'] = 2
    assert r.get('qwe') is 2
    assert r.get('w') is None
    assert r.get('w', 4) is 4
    assert type(r.keys()) is type({}.keys())
    assert list(r.keys()) == ['qwe']
    assert r._redis.dbsize() is 1
    assert r.pop('qwe') is 2
    with pytest.raises(KeyError):
        assert r.pop('qwe')
    assert r._redis.dbsize() is 0
    r['qwe'] = 2
    key, value = r.popitem()
    assert key == 'qwe'
    assert value is 2
    with pytest.raises(KeyError):
        r.popitem()
    assert r.setdefault('qwe', 1) is 1
    assert r.setdefault('qwe', 2) is 1
    assert list(r.keys()) == ['qwe']
    r.clear()
    r['qwe'] = 2
    r['qqq'] = 3
    r.update({'qwe':1, 'zzz':4})
    assert r._redis.dbsize() is 3
    assert r['qwe'] is 1
    assert r['qqq'] is 3
    assert r['zzz'] is 4
    assert 4 in list(r.values())
    assert 1 in list(r.values())
    assert 3 in list(r.values())
    assert r == {'qwe': 1, 'qqq': 3, 'zzz': 4}
    assert r != {'aaa': 1, 'bbb': 3, 'zzz': 5}
    assert r != {'qwe': 1, 'qqq': 3, 'zzz': 5}
    assert r != 1
    assert r != {'w': 2}
    its = r.items()
    assert type(its) == type({}.items())
    assert ('qwe', 1) in list(its)
    assert ('qqq', 3) in list(its)
    assert ('zzz', 4) in list(its)

    with pytest.raises(KeyError):
        r['rrr']

    with pytest.raises(NotImplementedError):
        r.fromkeys('qd')

    with pytest.raises(NotImplementedError):
        r.copy()

    r2 = Redpie()
    print(r2)
