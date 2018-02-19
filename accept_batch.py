from pathlib import Path
import argparse
import logging
import os
import subprocess
import sys
import yaml

from config import get_config


config = get_config()
sub_root = config.sub_root
asp_root = config.asp_root

"""
Arguement will be path where meta file is found
need to run in prod, since will call aspera
"""
#sub_base = Path('/stornext/snfs1/submissions/topmed')
#sub base will be defined in config now
g_base = Path(sub_root)
input_path= Path(sys.argv[1])
dest_path = Path(g_base, *input_path.parts[-5:])

input_path.glob('meta.{yaml,yml,txt}')
meta_hits = list(input_path.glob('meta.*'))
assert len(meta_hits) == 1,"There are too many meta hits"
meta_path = meta_hits[0]
meta_doc = yaml.load(meta_path.read_text())
#assert type(name) is StringType, "name is not a string: %r" % name

logging.basicConfig(level=logging.INFO)
class Generic:
    pass
meta = Generic()
meta.__dict__.update(meta_doc)

def print_tsv(tsv_file_path_str):
    spreadsheet_path=Path(tsv_file_path_str)
    sname = spreadsheet_path.name
    
    if input_file == sname:
        logging.info('TSV file: %s' % (sname))
    else:
        logging.warning('TSV file name in meta and in path do not match')                           
def is_cram(meta):
    "This bad boy ensures file format is just cram"
    ft = meta.file_formats[0]
    if ft.lower() == "cram":
        return True
    else:
        return False

def write_yaml(path):
    "This bad boy writes yaml files"
    meta_p = "meta.yaml"
    file_create= path / meta_p
    with file_create.open("w", encoding ="utf-8") as f:
        f.write("""state_id: 0 
      steps_completed: 0 
      state: 
        \t copy: initial 
        \t md5: initial 
        \t validation: initial \n""")
        return

def check_or_make(path):
    if path.exists():
        logging.warning("%s exist" % (path)) 
    else:
        path.mkdir(parents=True)

def aspera_path(input_p):
    cmd="scp -r "+ "meta.yaml" +" "+ aspd_base+"/"+batch_name+"/"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print (cmd)

def make_paths(input_path, dest_path):
    md5_path = Path(dest_path, 'md5')
    validation_path = Path(dest_path, 'validation')
    state_path = Path(dest_path, 'state')
    check_or_make(md5_path)
    check_or_make(validation_path)
    check_or_make(state_path)
    aspera_root = Path(asp_root,sub_proj,batch_name)
    check_or_make(aspera_root)


batch_name = meta.batch_title[7:]
batch_num = meta.batch_title[-3:-1]
sub_proj = meta.batch_title[7:-9]
project_code = meta.project_code
samp_num = meta.num_records
input_file = meta.input

if is_cram(meta) == True:
    #logging.info("This is a cram")
    make_paths(input_path, dest_path)
else:
    logging.error("!!Not a Cram!!!")


print_tsv(meta.input)
logging.info("PROJECT CODE: %s" % (project_code))
logging.info("FILE NAME: %s" % (meta_path.name))


