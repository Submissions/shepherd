from pathlib import Path
import argparse
import logging
import os
import sys
import yaml
"""
/groups/submissions/metadata/v1/topmed/phase3/cardia/01/17a/{md5,validation}
/groups/submissions/metadata/v1/topmed/phase3/cardia/01/17a/state/{00,current}.yaml
/aspera/share/globusupload/submissions/cardia/CARDIA_batch17a/meta.yaml
/stornext/submissions/topmed/md5-batches/CARDIA_batch17a/meta.yaml
/stornext/submissions/topmed/validation-batches/CARDIA_batch17a/meta.yaml
"""
input_file= sys.argv[1]
input_path= Path(input_file).absolute()
base_dirr =Path('')
base_dir = base_dirr.absolute()
print (base_dir)
meta_base = Path('/groups/submissions/metadata/v1/topmed')
sub_base = Path('/stornext/snfs1/submissions/topmed')
meta = "meta.yaml"

def write_yaml(path):
    "This bad boy writes yaml files"
    file_create= path / meta
    with file_create.open("w", encoding ="utf-8") as f:
        f.write("yaml /n")
        return

    
with open(input_file) as file:
    input=yaml.load(file)

test_path = input['Resources']['MyEC2Instance']['Type']
meta_test = input['Resources']['MyEC2Instance']['Properties']['KeyName']


#below makes directory will change "test" for the variable 
#below makes files in path I am writing
test_dir = base_dir / test_path
if test_dir.exists():
    
    print (base_dir)
    print ("base_dir above")
    
    write_yaml(test_dir)
    
else:
    test_dir.mkdir()
    write_yaml(test_dir)


meta_dir = meta_base / meta_test
if meta_dir.exists():
    print ("meta exist")

else:
    meta_dir.mkdir()

md5 = sub_base /"md5-batches"/meta_test
valid = sub_base /"validation-batches"/meta_test
if md5.exists():
    print ("md5 exist")

else:
    md5.mkdir()

if valid.exists():
    print ("valid exist")

else:
    valid.mkdir()



