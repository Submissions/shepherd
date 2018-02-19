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
    assert 'asp_root' in config
    assert 'sub_root' in config
    assert config['asp_root'] == accept_batch_fixture.asp_root
    assert config['sub_root'] == accept_batch_fixture.sub_root
    assert accept_batch_fixture.asp_root.isdir()
    assert accept_batch_fixture.sub_root.isdir()


def test_can_run_accept_batch(ran_accept_batch):
    pass


@mark.xfail()
def test_exit_0(ran_accept_batch):
    stdout.write(ran_accept_batch.stdout)
    stderr.write(ran_accept_batch.stderr)
    assert ran_accept_batch.returncode == 0


@mark.xfail()
def test_batch_dir(ran_accept_batch):
    """{temp_dir}/sub_root/topmed/phase3/biome/01/24a"""
    assert ran_accept_batch.batch_dir.isdir()


@mark.xfail()
def test_md5_dir(ran_accept_batch):
    """{temp_dir}/sub_root/topmed/phase3/biome/01/24a/md5"""
    md5_dir = ran_accept_batch.batch_dir / 'md5'
    assert md5_dir.isdir()


@mark.xfail()
def test_validation_dir(ran_accept_batch):
    """{temp_dir}/sub_root/topmed/phase3/biome/01/24a/validation"""
    validation_dir = ran_accept_batch.batch_dir / 'validation'
    assert validation.isdir()


@mark.xfail()
def test_state_dir(ran_accept_batch):
    """{temp_dir}/sub_root/topmed/phase3/biome/01/24a/state
    contents: current.yaml -> 00.yaml"""
    state_dir = ran_accept_batch.batch_dir / 'state'
    assert state_dir.isdir()
    state_file = state_dir / '00.yaml'
    assert state_file.isfile()
    assert state_file.read_text('ascii') == ran_accept_batch.state_00_contents
    current_link = state_dir / current.yaml
    assert current_link.islink()
    assert current_link.realpath() == state_file


def test_dest_dir(ran_accept_batch):
    """{temp_dir}/asp_root/BioMe/BioMe_batch24a
    contents: meta.yaml containing link to batch_dir"""
    assert ran_accept_batch.dest_dir.isdir()


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
        self.asp_root = self.root_dir.ensure_dir('asp_root')
        self.sub_root = self.root_dir.ensure_dir('sub_root')
        self.batch_dir = self.sub_root / 'topmed/phase3/biome/01/24a'
        self.dest_dir = self.asp_root / 'BioMe/BioMe_batch24a'
        # Main config file
        self.config_file = self.root_dir.join('config.yaml')
        config = dict(asp_root=str(self.asp_root), sub_root=str(self.sub_root))
        self.config_file.write_text(
            yaml.dump(config, default_flow_style=False), 'ascii')
        state_00_yaml = local('tests/resources/state_00.yaml')
        self.state_00_contents = state_00_yaml.read_text('ascii')
