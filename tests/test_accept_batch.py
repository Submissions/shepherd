from filecmp import cmp
from os import path
from subprocess import run, DEVNULL, PIPE
from sys import executable, stdout, stderr

from py.path import local
from pytest import fixture, mark
import yaml


def test_fixture(accept_batch_fixture):
    for k in sorted(vars(accept_batch_fixture)):
        print(k, getattr(accept_batch_fixture, k))
    with open(accept_batch_fixture.root_dir.join('config.yaml')) as fin:
        config = yaml.load(fin)
    print()
    for k in sorted(config):
        print(k, config[k])
    assert 'sub_root' in config


def test_can_run_accept_batch(ran_accept_batch):
    pass


@mark.xfail()
def test_exit_0(ran_accept_batch):
    stdout.write(ran_accept_batch.stdout)
    stderr.write(ran_accept_batch.stderr)
    assert ran_accept_batch.returncode == 0


@fixture(scope='module')
def ran_accept_batch(accept_batch_fixture):
    args = [executable, 'accept_batch.py', 'tests/resources/']
    cp = run(args, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, encoding='ascii',
             env=dict(SHEPHERD_CONFIG_FILE=accept_batch_fixture.config_file))
    accept_batch_fixture.stdout = cp.stdout
    accept_batch_fixture.stderr = cp.stderr
    accept_batch_fixture.returncode = cp.returncode
    return accept_batch_fixture


@fixture(scope='module')
def accept_batch_fixture(tmpdir_factory):
    return AcceptBatchFixture(tmpdir_factory)


class AcceptBatchFixture:
    def __init__(self, tmpdir_factory):
        self.root_dir = tmpdir_factory.mktemp('accept_batch')
        self.sub_root = self.root_dir.ensure_dir('sub_root')
        # Main config file
        self.config_file = self.root_dir.join('config.yaml')
        config = dict(sub_root=str(self.sub_root))
        self.config_file.write_text(
            yaml.dump(config, default_flow_style=False), 'ascii')
        meta_yaml_src = local('tests/resources/meta.yaml')
        # meta_yaml_src.copy(meta_yaml_dst)
        # Aspera path
