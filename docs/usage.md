Customer:

    cd /groups/project-managers/tech/metadata/v1/topmed/phase3/cardia/01/17a
    send_batch CARDIA_batch17a_globus.tsv

Effects:

* Reads:
  - `defaults.yaml` in parent directories through `topmed`
  - CARDIA_batch17a_globus.tsv
* Fetches sizes of all CRAM files.
* Creates:
  - sub -> ../../../../../sub/v1/topmed/phase3/cardia/01/17a
  - meta.yaml
* Outputs:
  - summary stats
  - WORKLIST for {output file}
  - blank line
  - absolute path of new directory (17a in this case)
  - blank line
  - contents of meta.yaml

Submissions:

    accept_batch /groups/project-managers/tech/metadata/v1/topmed/phase3/cardia/01/17a

Effects:

* Reads: /groups/project-managers/tech/metadata/v1/topmed/phase3/cardia/01/17a/meta.yaml
* Asserts just CRAM for file_formats
* Creates:
    - /groups/submissions/metadata/v1/topmed/phase3/cardia/01/17a/{md5,validation}
    - /groups/submissions/metadata/v1/topmed/phase3/cardia/01/17a/state/{00,current}.yaml
    - /aspera/share/globusupload/submissions/cardia/CARDIA_batch17a/meta.yaml
* Outputs:
    - input TSV file name
    - `funding_code`
    - `project_code`

Run scripts as normal, except that input is now TSV.

As things succeed, run:

    cd $SOME_WORKING_DIR
    update_batch
