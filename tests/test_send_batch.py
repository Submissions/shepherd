from pytest import fixture


def test_a(send_batch):
    assert 0, send_batch


def test_b(send_batch):
    assert 0, send_batch


@fixture(scope='module')
def send_batch(tmpdir_factory):
    return tmpdir_factory.mktemp('send_batch')
