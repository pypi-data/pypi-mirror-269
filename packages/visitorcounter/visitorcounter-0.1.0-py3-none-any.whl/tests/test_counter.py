from visitorcounter import VisitorCounter

def test_visits():
    vc = VisitorCounter()
    assert vc.visit() == 1
    assert vc.visit() == 2
    assert vc.get_count() == 2
