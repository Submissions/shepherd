from datetime import date, timedelta
from filecmp import cmp
from os import path
from subprocess import run, DEVNULL, PIPE
from sys import executable, stdout, stderr

from py.path import local
from pytest import fixture
import yaml


# Note that pm_root is not coming from config. It is a test-only concept,
# representing the directory that contains the `sub` symlink and and the
# top-level project directory.

def test_fixture(send_batch_fixture):
    for k in sorted(vars(send_batch_fixture)):
        print(k, getattr(send_batch_fixture, k))
    with open(send_batch_fixture.root_dir.join('config.yaml')) as fin:
        config = yaml.load(fin)
    print()
    for k in sorted(config):
        print(k, config[k])
    assert 'sub_root' in config
    send_batch_fixture.sub_root.isdir()
    pm_root = send_batch_fixture.pm_root
    assert pm_root.join('topmed/phase3/biome/01/24a').isdir()


def test_can_run_send_batch(ran_send_batch):
    pass  # If we get here, that just proves we could run send_batch.py.


def test_send_batch_returned_0(ran_send_batch):
    stderr.write(ran_send_batch.stderr)
    stdout.write(ran_send_batch.stdout)
    assert ran_send_batch.returncode == 0


def test_batch_symlink(ran_send_batch):
    link_path = ran_send_batch.batch_path/'sub'
    assert link_path.islink()
    assert link_path.isdir()
    assert link_path.realpath() == ran_send_batch.sub_batch_path
    expected_link = '../../../../../sub/topmed/phase3/biome/01/24a'
    assert link_path.readlink() == expected_link


def test_meta_yaml(ran_send_batch, yesterday_and_today):
    """Expect:
        batch_title: TOPMed_BioMe_batch24a
        input: BioMe_batch24a_mplx.tsv
        batch_date: 2018-01-24 (whatever today's date is)
        file_formats:
            - CRAM
        num_records: 10
        file_sizes: 0-0G
        attempt: a
        funding_source: TOPMED_phase3_123456
        project_code: proj-dm0019
    """
    meta_path = ran_send_batch.batch_path/'meta.yaml'
    assert meta_path.isfile()
    with open(meta_path) as fin:
        meta_dict = yaml.load(fin)
    meta = Generic()
    meta.__dict__.update(meta_dict)
    assert meta.input == 'BioMe_batch24a_mplx.tsv'
    d = yesterday_and_today.d
    assert d.yesterday <= meta.batch_date <= d.today
    assert meta.file_formats == ['CRAM']
    assert meta.num_records == 10
    assert meta.file_sizes == '0-0G'
    assert meta.attempt == 'a'
    assert meta.funding_source == 'TOPMed Phase III_1355'
    assert meta.project_code == 'proj-dm0019'
    assert meta.batch_title == 'TOPMed_BioMe_batch24a'


def test_no_error(ran_send_batch):
    stderr.write(ran_send_batch.stderr)
    assert not ran_send_batch.stderr


def test_output(ran_send_batch, yesterday_and_today):
    with open('tests/resources/send_batch_output.txt') as fin:
        template = fin.read()
    s = yesterday_and_today.s
    expect_y = template.format(pm_root=ran_send_batch.pm_root,
                               today=s.yesterday)
    expect_t = template.format(pm_root=ran_send_batch.pm_root,
                               today=s.today)
    stdout = ran_send_batch.stdout
    print(repr(stdout))
    print('===============')
    print(repr(expect_t))
    assert (stdout == expect_t) or (stdout == expect_y)


@fixture(scope='module')
def yesterday_and_today():
    """Prode `date` (d) and `str` (s) versions of yesterday and today."""
    d = Generic()
    d.today = date.today()
    d.yesterday = d.today - timedelta(1)
    s = Generic()
    s.today = d.today.isoformat()
    s.yesterday = d.yesterday.isoformat()
    result = Generic()
    result.d = d
    result.s = s
    return result


class Generic:
    """Just to wrap a dict"""


@fixture(scope='module')
def ran_send_batch(send_batch_fixture):
    args = [executable,
            local('send_batch.py'),
            send_batch_fixture.batch_path/'BioMe_batch24a_mplx.tsv']
    cp = run(args, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, encoding='ascii',
             env=dict(SHEPHERD_CONFIG_FILE=send_batch_fixture.config_file),
             cwd=send_batch_fixture.batch_path)
    send_batch_fixture.stdout = cp.stdout
    send_batch_fixture.stderr = cp.stderr
    send_batch_fixture.returncode = cp.returncode
    return send_batch_fixture


@fixture(scope='module')
def send_batch_fixture(tmpdir_factory):
    return SendBatchFixture(tmpdir_factory)


class SendBatchFixture:
    def __init__(self, tmpdir_factory):
        # Main directories
        self.resources_path = local('tests/resources')
        self.root_dir = tmpdir_factory.mktemp('send_batch')
        self.pm_root = self.root_dir.ensure_dir('pm_root')
        self.sub_root = self.root_dir.ensure_dir('sub_root')
        phase3_path = self.pm_root/'topmed/phase3'
        biome_path = phase3_path/'biome'
        group_path = phase3_path/'biome/01'
        self.batch_path = group_path.ensure_dir('24a')
        self.sub_batch_path = self.sub_root/'topmed/phase3/biome/01/24a'
        self.sub_batch_path.ensure_dir()
        # Main config file
        self.config_file = self.root_dir.join('config.yaml')
        config = dict(asp_root=None, sub_root=str(self.sub_root))
        self.config_file.write_text(
            yaml.dump(config, default_flow_style=False), 'ascii'
        )
        # defaults.yaml
        self.copy_resource('defaults_phase3.yaml', phase3_path/'defaults.yaml')
        self.copy_resource('defaults_biome.yaml', biome_path/'defaults.yaml')
        # Input TSV
        self.raw_worklist_path = self.resources_path/'BioMe_batch24am.tsv'
        self.generated_worklist_path = generate_worklist(self.batch_path)
        # Symlink between pm_root and sub_root
        self.pm_root.join('sub').mksymlinkto('../sub_root')

    def copy_resource(self, src_str, dst_path):
        src_path = self.resources_path / src_str
        src_path.copy(dst_path)


def generate_worklist(dest_dir):
    with open('tests/resources/BioMe_batch24am_mplx.tsv') as fin:
        template = fin.read()
    dest_path = dest_dir.join('BioMe_batch24a_mplx.tsv')
    with dest_path.open('w', 'ascii') as fout:
        fout.write(
            template.format(crams=path.abspath('tests/resources/crams'))
        )
    return dest_path
