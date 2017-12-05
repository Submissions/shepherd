At start:

    submission_kickoff /groups/project-managers/metadata/v1/topmed/phase3/cardia/01/17a

Effects:

* Reads: /groups/project-managers/metadata/v1/topmed/phase3/cardia/01/17a/meta.yaml3
* Asserts just CRAM for file_formats
* Creates:
    - /groups/submissions/metadata/v1/topmed/phase3/cardia/01/17a/{md5,validation}
    - /groups/submissions/metadata/v1/topmed/phase3/cardia/01/17a/state/{00,current}.yaml
    - /aspera/share/globusupload/submissions/cardia/CARDIA_batch17a/meta.yaml
    - /stornext/submissions/topmed/md5-batches/CARDIA_batch17a/meta.yaml
    - /stornext/submissions/topmed/validation-batches/CARDIA_batch17a/meta.yaml
* Outputs:
    - input TSV file name
    - `funding_code`
    - `project_code`

Run scripts as normal, except that input is now TSV.

As things succeed, run:

    cd $SOME_WORKING_DIR
    submission_update
