from pytest import fixture
import yaml


def test_fixture(accept_batch_fixture):
    for k in sorted(vars(accept_batch_fixture)):
        print(k, getattr(accept_batch_fixture, k))
    with open(accept_batch_fixture.root_dir.join('config.yaml')) as fin:
        config = yaml.load(fin)
    print()
    for k in sorted(config):
        print(k, config[k])
    assert 'pm_root' in config
    assert 'sub_root' in config


@fixture(scope='module')
def accept_batch_fixture(tmpdir_factory):
    return AcceptBatchFixture(tmpdir_factory)


class AcceptBatchFixture:
    def __init__(self, tmpdir_factory):
        self.root_dir = tmpdir_factory.mktemp('accept_batch')
        self.pm_root = self.root_dir.join('pm_root')
        self.sub_root = self.root_dir.join('sub_root')
        self.config_file = self.root_dir.join('config.yaml')
        config = dict(pm_root=str(self.pm_root), sub_root=str(self.sub_root))
        self.config_file.write_text(
            yaml.dump(config, default_flow_style=False), 'ascii'
        )
