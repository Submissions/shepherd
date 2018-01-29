#!/usr/bin/env python3

import os
import sys
import shutil
from pathlib import Path
import yaml
import datetime

from config import get_config


# Parse the last 5 directories in the absolute path.
here = Path().absolute()
project_name, phase, subproject_name, batch_group, batch_name = here.parts[-5:]

batch_input_file = sys.argv[1]

sizes = []

with open(batch_input_file) as f:
    next(f)
    for raw_line in f:
        line = raw_line.rstrip().split("\t")
        cram_paths = line[8]
        extension = cram_paths.split(".")[-1]
        s = (os.path.getsize(cram_paths))
        sizes.append(s)
        min_size = min(sizes)
        gb_min_size = round(min_size/2**30)
        max_size = max(sizes)
        gb_max_size = round(max_size / 2**30)
        size_range = str(gb_min_size) + '-' + str(gb_max_size) + 'G'
        num_records = len(sizes)

batch_group_path = here.parent

with open(batch_group_path/'defaults.yaml') as f:
    d = yaml.load(f)
funding = d['funding_source']
project_code = d['project_code']

sub_path = here/'sub'
sub_path.symlink_to(
    '../../../../../sub/{}/{}/{}/{}/{}'.format(
        *(here.parts[-5:])
    )
)

d = dict(input=os.path.basename(batch_input_file),
         num_records=num_records,
         file_sizes=size_range,
         funding_source = funding,
         project_code = project_code,
         batch_date = datetime.date.today(),
         attempt = batch_name[-1],
         file_formats = [extension.upper()],
         batch_title = 'TOPMed_' + subproject_name.upper()
         + '_batch' + batch_name)
# TODO: Hardcoded "TOPMed" into batch_title.

meta_path = here/'meta.yaml'
with open(meta_path, 'w') as fout:
    yaml.dump(d, fout, default_flow_style=False)

print(num_records, 'records')
print(size_range)
print()
print('WORKLIST for ' + os.path.basename(batch_input_file))
print()
print(os.path.abspath(here))
print()
with open(meta_path) as f:
    text = f.read()
    sys.stdout.write(text)
