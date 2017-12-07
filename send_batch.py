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

subprocess.Popen(['mkdir', '-p','project_name/phase/subproject_name/batch_group/batch_name'])
