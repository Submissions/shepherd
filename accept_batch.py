from pathlib import Path
import argparse
import logging
import os
import sys
import yaml
"""
Arguement will be path where meta file is found
need to run in prod, since will call aspera
/groups/submissions/metadata/v1/topmed/phase3/cardia/01/17a/{md5,validation}
/groups/submissions/metadata/v1/topmed/phase3/cardia/01/17a/state/{00,current}.yaml
/aspera/share/globusupload/submissions/cardia/CARDIA_batch17a/meta.yaml
/stornext/submissions/topmed/md5-batches/CARDIA_batch17a/meta.yaml
/stornext/submissions/topmed/validation-batches/CARDIA_batch17a/meta.yaml
"""
sub_base = Path('/stornext/snfs1/submissions/topmed/test')
#asp_base = Path('/aspera/share/share/globusupload/submissions/test') #Might need to run in prod
asp_base = Path('aspera/share/globusupload/submissions')
g_base = Path('/groups/submissions/metadata/v1')
base_dirr =Path('')
base_dir = base_dirr.absolute()
input_path= Path(sys.argv[1])
input_path.glob('meta.{yaml,yml,txt}')
meta_hits = list(input_path.glob('meta.*'))
assert len(meta_hits) == 1, meta_hits
meta_path = meta_hits[0]
meta_doc = yaml.load(meta_path.read_text())


class Generic:
    pass
meta = Generic()
meta.__dict__.update(meta_doc)

def is_cram(meta):
    "This bad boy ensures file format is just cram"
    ft = meta.file_formats[0]
    assert ft.lower() == "cram"


def write_yaml(path):
    "This bad boy writes yaml files"
    meta_p = "meta.yaml"
    file_create= path / meta_p
    with file_create.open("w", encoding ="utf-8") as f:
        f.write("yaml /n")
        return

def check_or_make(path):
    if path.exists():
        print ("%s exist" % (path)) 
        write_yaml(path)
    else:
        path.mkdir(parents=True)
        write_yaml(path)
def make_paths(input_p):
    md5_g = Path(input_p,"md5")
    check_or_make(md5_g)
    val_g = Path(input_p,"validation")
    check_or_make(val_g)
    #asp = Path(asp_base,sub_proj,batch_name)
    #check_or_make(asp)
    md5_s = Path(sub_base,"md5-batches",batch_name)
    val_s = Path(sub_base,"validation-batches",batch_name)
    check_or_make(md5_s)
    check_or_make(val_s)


batch_name = meta.batch_title[7:]
batch_num = meta.batch_title[-3:-1]
sub_proj = meta.batch_title[7:-9]
project_code = meta.project_code
samp_num = meta.num_records


make_paths(input_path)

dest_path = Path(g_base, *input_path.parts[-5:])


#dest_path.mkdir(parents=True, exist_ok=True)
#write_yaml(dest_path)





