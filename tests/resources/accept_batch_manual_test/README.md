Run this test from the project root.

Uses `tests/resources/accept_batch_manual_test/topmed/phase3/biome/01/24a` as
input of testing code

This adds the required paths in config file and runs the test manually:

    SHEPHERD_CONFIG_FILE=tests/resources/accept_batch_manual_test/config.yaml \
    python3 accept_batch.py \
    tests/resources/accept_batch_manual_test/topmed/phase3/biome/01/24a
