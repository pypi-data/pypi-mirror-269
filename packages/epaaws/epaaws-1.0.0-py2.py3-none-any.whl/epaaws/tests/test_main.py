def check(f):
    assert f.sizes['TSTEP'] == 1
    assert f.sizes['LAY'] == 1
    assert f.sizes['ROW'] == 299
    assert f.sizes['COL'] == 459
    assert 'HT' in f.data_vars


def test_opendate():
    from ..util import open_date
    bucket = 'epa-2022-modeling-platform'
    tmpl = 'MCIP/GRIDCRO2D.12US1.35L.%y%m%d'
    f = open_date('2022-01-02', tmpl, bucket)
    check(f)


def test_mp2022():
    from ..mp2022 import open_gridcro2d
    f = open_gridcro2d('2022-01-01')
    check(f)
