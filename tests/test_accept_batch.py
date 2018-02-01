from filecmp import cmp
from os import path
from subprocess import run, DEVNULL, PIPE
from sys import executable, stdout, stderr

from py.path import local
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


def test_can_run_accept_batch(ran_accept_batch):
    pass


@fixture(scope='module')
def ran_accept_batch(accept_batch_fixture):
    args = [executable, 'accept_batch.py', 'tests/resources/']
    cp = run(args, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, encoding='ascii', env=dict(SHEPHERD_CONFIG_FILE=accept_batch_fixture.config_file))
    accept_batch_fixture.stdout = cp.stdout
    accept_batch_fixture.stderr = cp.stderr
    assert cp.returncode == 0
    return accept_batch_fixture


@fixture(scope='module')
def accept_batch_fixture(tmpdir_factory):
    return AcceptBatchFixture(tmpdir_factory)


class AcceptBatchFixture:
    def __init__(self, tmpdir_factory):
        self.root_dir = tmpdir_factory.mktemp('accept_batch')
        self.pm_root = self.root_dir.join('pm_root')
        self.sub_root = self.root_dir.join('sub_root')
        group_path = self.pm_root/'tests/resources/'
        group_path.ensure_dir()
        self.batch_path = group_path/'24a'
        self.sub_batch_path = self.sub_root/'topmed/phase3/tmsol/01/24a'
        self.sub_batch_path.ensure_dir()
        # Main config file
        self.config_file = self.root_dir.join('config.yaml')
        config = dict(pm_root=str(self.pm_root), sub_root=str(self.sub_root))
        self.config_file.write_text(
            yaml.dump(config, default_flow_style=False), 'ascii')
        # send_meta.yaml
        send_meta_yaml_path = group_path/'send_meta.yaml'
        send_meta_yaml_src = local('tests/resources/send_meta.yaml')
        send_meta_yaml_src.copy(send_meta_yaml_path)
        # Aspera path