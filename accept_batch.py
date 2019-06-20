#!/usr/bin/env python3

import argparse
import logging
import shutil
import subprocess
import sys
import yaml
from pathlib import Path

from config import get_config


def main():
    args = parse_args()
    configure_logging()
    run(args.working_path)
    sys.exit(0)


def configure_logging():
    global logger
    err_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    err_handler.setFormatter(formatter)
    logger = logging.getLogger("shepherd.accept_batch")
    logger.addHandler(err_handler)
    logger.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("working_path")
    args = parser.parse_args()
    return args


def run(input_path):
    # Get config paths
    config = get_config()
    sub_root = Path(config.sub_root)
    asp_root = config.asp_root
    input_path = Path(input_path)
    dest_path = Path(sub_root, *input_path.parts[-5:])

    # Get meta info
    meta_path = get_meta_file(input_path)
    meta = dict(yaml.safe_load(meta_path.read_text()))

    try:
        batch_name = meta["batch_title"][7:]
        batch_num = meta["batch_title"][-3:-1]
        sub_proj = meta["batch_title"][7:-9]
        project_code = meta["project_code"]
        samp_num = meta["num_records"]
        input_file = meta["input"]
    except KeyError:
        logger.exception("Missing key from meta file.")
        sys.exit(1)

    # Check that the tsv file exist
    if not Path(input_path, input_file).exists():
        logger.error(f"TSV file {input_file} does not exist.")
        sys.exit(1)

    # Check thats the file is a CRAM
    if is_cram(meta["file_formats"]):
        make_paths(asp_root, batch_name, dest_path, sub_proj)

    # Copy over TSV input file to destination path
    shutil.copy(Path(input_path, input_file), dest_path)

    logger.info("PROJECT CODE: %s" % (project_code))
    logger.info("FILE NAME: %s" % (meta_path.name))
    logger.info("Batch successfully accepted.")


def get_meta_file(input_path):
    meta_hits = list(input_path.glob("meta.*"))
    if len(meta_hits) > 1:
        logger.error("There are too many meta hits.")
        sys.exit(1)
    elif len(meta_hits) == 0:
        logger.error("No meta hits were found.")
        sys.exit(1)
    else:
        return meta_hits[0]


def is_cram(file_formats):
    """This bad boy ensures file format is just cram"""
    for file in file_formats:
        if file.lower() != "cram":
            logger.error("This is not a CRAM!")
            sys.exit(1)
    return True


def make_paths(asp_root, batch_name, dest_path, sub_proj):
    md5_path = Path(dest_path, "md5")
    validation_path = Path(dest_path, "validation")
    state_path = Path(dest_path, "state")
    check_or_make(md5_path)
    check_or_make(validation_path)
    check_or_make(state_path)
    write_yaml(state_path)
    link_current_path = state_path / "current.yaml"
    link_current_path.symlink_to("00.yaml")
    aspera_root = Path(asp_root, sub_proj, batch_name)
    check_or_make(aspera_root)


def check_or_make(path):
    if path.exists():
        logger.warning("Path %s exist" % (path))
        sys.exit(1)
    else:
        path.mkdir(parents=True)


def aspera_path(input_p):
    # TODO: Check if being used anywhere by other app, otherwise delete.
    cmd="scp -r "+ "meta.yaml" +" "+ aspd_base+"/"+batch_name+"/"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print (cmd)


def write_yaml(path):
    """This bad boy writes yaml files"""
    file_create = path / "00.yaml"
    data = {
        "state_id": 0,
        "steps_completed": 0,
        "state": {"copy": "initial", "md5": "initial", "validation": "initial"},
    }
    with open(file_create, "w") as outfile:
        yaml.dump(data, outfile, sort_keys=False)


if __name__ == "__main__":
    main()
