from os import path
from subprocess import run, DEVNULL, PIPE
from sys import executable, stdout, stderr

import jinja2
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


@fixture(scope='module')
def ran_send_batch(send_batch_fixture):
    args = [executable,
            'send_batch.py',
            'topmed', '3', 'tmsol', '01', '24a',
            'tests/resources/TMSOL_batch24am.tsv',
            send_batch_fixture.root_dir/'TMSOL_batch24a_cram.tsv']
    cp = run(args, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, encoding='ascii',
             env=dict(SHEPHERD_CONFIG_FILE=send_batch_fixture.config_file))
    stdout.write(cp.stdout)
    stderr.write(cp.stderr)
    assert cp.returncode == 0
    return send_batch_fixture


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
        generate_worklist(self.root_dir)


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
