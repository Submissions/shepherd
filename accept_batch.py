from pathlib import Path
import argparse
import logging
import os
#import sh
import sys
import yaml
"""
Arguement will be path where meta file is found
need to run in prod, since will call aspera
"""
sub_base = Path('/stornext/snfs1/submissions/topmed')
asp_base = Path('/aspera/share/globusupload/submissions/test')
aspd_base="christis@hgsc-aspera1.hgsc.bcm.edu:/share/share/globusupload/submissions"
g_base = Path('/groups/submissions/metadata/v1')
input_path= Path(sys.argv[1])
dest_path = Path(g_base, *input_path.parts[-5:])
input_path.glob('meta.{yaml,yml,txt}')
meta_hits = list(input_path.glob('meta.*'))
assert len(meta_hits) == 1,"There are too many meta hits"
meta_path = meta_hits[0]
meta_doc = yaml.load(meta_path.read_text())
dest_path = Path(g_base, *input_path.parts[-5:])
#assert type(name) is StringType, "name is not a string: %r" % name

logging.basicConfig(level=logging.INFO)
class Generic:
    pass
meta = Generic()
meta.__dict__.update(meta_doc)

def find_tsv(input_p):
    spreadsheet_hits= list(input_p.glob('*.tsv'))
    assert len(spreadsheet_hits) == 1,"There are too many meta hits"
    spreadsheet_path=spreadsheet_hits[0]
    sname = spreadsheet_path.name
    logging.info('TSV file: %s"' % (sname))

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
        write_yaml(path)
    else:
        path.mkdir(parents=True)
        write_yaml(path)

def aspera_path(path):
    #christis@hgsc-aspera1.hgsc.bcm.edu:/share/share/globusupload/submissions/$batch_type/$batch_name/
    cmd="mkdir -p "+aspd_base +"/"+sub_proj+"/"+batch_name
    os.system(cmd)

def make_paths(input_p):
    md5_g = Path(input_p,"md5")
    check_or_make(md5_g)
    val_g = Path(input_p,"validation")
    check_or_make(val_g)
    asp = Path(asp_base,sub_proj,batch_name)
    check_or_make(asp)
    md5_s = Path(sub_base,"md5-batches",batch_name)
    val_s = Path(sub_base,"validation-batches",batch_name)
    check_or_make(md5_s)
    check_or_make(val_s)

batch_name = meta.batch_title[7:]
batch_num = meta.batch_title[-3:-1]
sub_proj = meta.batch_title[7:-9]
project_code = meta.project_code
samp_num = meta.num_records

if is_cram(meta) == True:
    #logging.info("This is a cram")
    make_paths(input_path)
else:
    logging.error("!!Not a Cram!!!")

find_tsv(input_path)

logging.info("PROJECT CODE: %s" % (project_code))
logging.info("FILE NAME: %s" % (meta_path.name))
#logging.info('TSV NAME: %S' % (find_tsv(input_path))) 
#aspera_path(input_path)
