from cjen.nene.collection_utils import list_eql


def test_list_eql():
    assert list_eql([1, 2], [2, 1]) == True
    assert list_eql([dict(id=2), dict(id=1)], [dict(id=1), dict(id=2)]) == True
    assert list_eql([dict(id=2), dict(id=1)], [dict(id=1), dict(id=2)]) == True
    assert list_eql([[1, 2], [3, 4]], [[3, 4], [1, 2]]) == True
    # assert list_eql([[1,2], [3,4]], [[2,1], [4,3]]) == True
