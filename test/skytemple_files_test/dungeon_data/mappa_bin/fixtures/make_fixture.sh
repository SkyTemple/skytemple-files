#!/usr/bin/env bash
set -ex

# This makes the fixture.bin and a Python module (fixture_autogen) that contains
# the fixtures.
python make_fixture.py > ../fixture_autogen.py
