from datetime import date, timedelta
from filecmp import cmp
from os import path
from subprocess import run, DEVNULL, PIPE
from sys import executable, stdout, stderr

import jinja2
from py.path import local
from pytest import fixture
import yaml


def test_fixture(send_batch_fixture):
    for k in sorted(vars(send_batch_fixture)):
        print(k, getattr(send_batch_fixture, k))
    with open(send_batch_fixture.root_dir.join('config.yaml')) as fin:
        config = yaml.load(fin)
    print()
    for k in sorted(config):
        print(k, config[k])
    assert 'pm_root' in config
    assert 'sub_root' in config


def test_can_run_send_batch(ran_send_batch):
    pass  # If we get here, that just proves we could run send_batch.py.


def test_pm_root_created(ran_send_batch):
    print(ran_send_batch.stdout)
    assert ran_send_batch.pm_root.isdir()


def test_batch_dir_created(ran_send_batch):
    assert ran_send_batch.pm_root.join('topmed/phase3/tmsol/01/24a').isdir()


def test_batch_files_copied(ran_send_batch):
    raw_path = ran_send_batch.batch_path/'TMSOL_batch24am.tsv'
    cram_path = ran_send_batch.batch_path/'TMSOL_batch24a_cram.tsv'
    cmp(ran_send_batch.raw_worklist_path, raw_path)
    cmp(ran_send_batch.generated_worklist_path, cram_path)


def test_batch_symlink(ran_send_batch):
    link_path = ran_send_batch.batch_path/'sub'
    assert link_path.islink()
    assert link_path.isdir()
    assert link_path.realpath() == ran_send_batch.sub_batch_path
    expected_link = '../../../../../sub/topmed/phase3/tmsol/01/24a'
    assert link_path.readlink() == expected_link


def test_meta_yaml(ran_send_batch):
    """Expect:
        batch_title: TOPMed_TMSOL_batch24a
        input: TMSOL_batch24a_cram.tsv
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
    assert meta.input == 'TMSOL_batch24a_cram.tsv'
    today = date.today()
    yesterday = today - timedelta(1)
    assert yesterday <= meta.batch_date <= today
    assert meta.file_formats == ['CRAM']
    assert meta.num_records == 10
    assert meta.file_sizes == '0-0G'
    assert meta.attempt == 'a'
    assert meta.funding_source == 'TOPMED_phase3_123456'
    assert meta.project_code == 'proj-dm0019'
    assert meta.batch_title == 'TOPMed_TMSOL_batch24a'


class Generic:
    """Just to wrap a dict"""


def test_no_error(ran_send_batch):
    assert not ran_send_batch.stderr


def test_output(ran_send_batch):
    # print(ran_send_batch.stdout)
    with open('tests/resources/send_batch_output.txt') as fin:
        template_str = fin.read()
    template = jinja2.Template(template_str)
    expect = template.render(pm_root=ran_send_batch.pm_root,
                             today=date.today().isoformat()) + '\n'
    # TODO: Handle Jinja2 stripping the trailing newline better.
    # TODO: Race condidion if run at midnight.
    print('===============')
    print(repr(ran_send_batch.stdout))
    print('===============')
    print(repr(expect))
    assert ran_send_batch.stdout == expect


@fixture(scope='module')
def ran_send_batch(send_batch_fixture):
    args = [executable,
            'send_batch.py',
            'topmed', 'phase3', 'tmsol', '01', '24a',
            'tests/resources/TMSOL_batch24am.tsv',
            send_batch_fixture.root_dir/'TMSOL_batch24a_cram.tsv']
    cp = run(args, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, encoding='ascii',
             env=dict(SHEPHERD_CONFIG_FILE=send_batch_fixture.config_file))
    send_batch_fixture.stdout = cp.stdout
    send_batch_fixture.stderr = cp.stderr
    assert cp.returncode == 0
    return send_batch_fixture


@fixture(scope='module')
def send_batch_fixture(tmpdir_factory):
    return SendBatchFixture(tmpdir_factory)


class SendBatchFixture:
    def __init__(self, tmpdir_factory):
        # Main directories
        self.root_dir = tmpdir_factory.mktemp('send_batch')
        self.pm_root = self.root_dir.ensure_dir('pm_root')
        self.sub_root = self.root_dir.ensure_dir('sub_root')
        group_path = self.pm_root/'topmed/phase3/tmsol/01'
        group_path.ensure_dir()
        self.batch_path = group_path/'24a'
        self.sub_batch_path = self.sub_root/'topmed/phase3/tmsol/01/24a'
        self.sub_batch_path.ensure_dir()
        # Main config file
        self.config_file = self.root_dir.join('config.yaml')
        config = dict(pm_root=str(self.pm_root), sub_root=str(self.sub_root))
        self.config_file.write_text(
            yaml.dump(config, default_flow_style=False), 'ascii'
        )
        # defaults.yaml
        defaults_yaml_path = group_path/'defaults.yaml'
        defaults_yaml_src = local('tests/resources/defaults.yaml')
        defaults_yaml_src.copy(defaults_yaml_path)
        # Input TSV
        self.raw_worklist_path = local('tests/resources/TMSOL_batch24am.tsv')
        self.generated_worklist_path = generate_worklist(self.root_dir)
        # Symlink between pm_root and sub_root
        self.pm_root.join('sub').mksymlinkto('../sub_root')


def generate_worklist(dest_dir):
    with open('tests/resources/TMSOL_batch24am_cram.tsv') as fin:
        template_str = fin.read()
    template = jinja2.Template(template_str)
    dest_path = dest_dir.join('TMSOL_batch24a_cram.tsv')
    with dest_path.open('w', 'ascii') as fout:
        fout.write(
            template.render(crams=path.abspath('tests/resources/crams'))
        )
        fout.write('\n')
    return dest_path
