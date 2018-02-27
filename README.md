# shepherd

version 0.2.0-rc2

A set of scripts for defining batches of work that are then tracked to failure
or (possibly partial) completion.

Currently implemented:

* `send_batch`: evaluates a batch TSV file and generates the YAML batch file.

## `send_batch`

`send_batch` looks 4 levels up the tree looking for files named
`defaults.yaml`. Any such files found are accumulated into a ("defaults")
dictionary. Values in lower level directories supplant corresponding values in
higher level directories. The resulting `project_name` and `subproject_name`
values form a part of the generated batch name.

Example:

    cd /groups/project-managers/topmed/phase3/cardia/01/17a
    send_batch CARDIA_batch17a_globus.tsv

Required:

* combined `defaults.yaml`:
  - project_name
  - subproject_name
  - funding_source
  - project_code
* header of the TSV file:
  - cram_path

Effects:

* Reads:
  - `defaults.yaml` in parent directories through `topmed`
  - `CARDIA_batch17a_globus.tsv`
* Fetches sizes of all CRAM files.
* Creates:
  - `sub` -> `../../../../../sub/v1/topmed/phase3/cardia/01/17a`
  - `meta.yaml`

Output:

    100 records
    22-25G

    WORKLIST for CARDIA_batch17a_globus.tsv

    /groups/project-managers/topmed/phase3/cardia/01/17a

    attempt: a
    batch_date: {today}
    batch_title: TOPMed_TMSOL_batch24a
    file_formats:
    - CRAM
    file_sizes: 0-0G
    funding_source: TOPMED_phase3_123456
    input: TMSOL_batch24a_cram.tsv
    num_records: 10
    project_code: proj-dm0019
