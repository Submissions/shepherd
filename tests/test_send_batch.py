from pytest import fixture
import yaml


def test_a(send_batch_fixture):
    for k in sorted(vars(send_batch_fixture)):
        print(k, getattr(send_batch_fixture, k))
    with open(send_batch_fixture.root_dir.join('config.yaml')) as fin:
        config = yaml.load(fin)
    print()
    for k in sorted(config):
        print(k, config[k])
    assert 'pm_root' in config
    assert 'sub_root' in config
    assert 0


def test_b(send_batch_fixture):
    pass


@fixture(scope='module')
def send_batch_fixture(tmpdir_factory):
    return SendBatchFixture(tmpdir_factory)


class SendBatchFixture:
    def __init__(self, tmpdir_factory):
        self.root_dir = tmpdir_factory.mktemp('send_batch')
        self.pm_root = self.root_dir.join('pm_root')
        self.sub_root = self.root_dir.join('sub_root')
        self.config_file = self.root_dir.join('config.yaml')
        config = dict(pm_root=str(self.pm_root), sub_root=str(self.sub_root))
        self.config_file.write_text(
            yaml.dump(config, default_flow_style=False), 'ascii'
        )
