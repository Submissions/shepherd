#!/usr/bin/env python3.6

import os
import sys
from pathlib import Path

project_name = sys.argv[1]
phase = sys.argv[2]
subproject_name = sys.argv[3]
batch_group = sys.argv[4]
batch_name = sys.argv[5]
batch_input_file = sys.argv[6]
globus_input_file = sys.argv[7]


sizes = []

with open(batch_input_file) as f:
    next(f)
    for raw_line in f:
        line = raw_line.rstrip().split("\t")
        cram_paths = line[7]
        s = (os.path.getsize(cram_paths))
        sizes.append(s)
        min_size = min(sizes)
        max_size = max(sizes)
        num_records = len(sizes)
print(min_size, max_size, num_records) #TODO: convert to GB?

pr = Path(project_name)
ph = phase
sn = subproject_name
bg = batch_group
bn = batch_name

batch_path = Path(pr/ph/sn/bg/bn)

batch_path.mkdir(exist_ok=True, parents=True)
