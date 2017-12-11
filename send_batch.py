#!/usr/bin/env python2.7

import os
import sys
import subprocess

project_name = sys.argv[1]
phase = sys.argv[2]
subproject_name = sys.argv[3]
batch_group = sys.argv[4]
batch_name = sys.argv[5]
batch_input_file = sys.argv[6]
globus_input_file = sys.argv[7]

with open(batch_input_file) as f:
    next(f)
    for raw_line in f:
        line = raw_line.rstrip().split("\t")
        cram_paths = line[7]
        sizes = []
        sizes.append(os.path.getsize(cram_paths)
