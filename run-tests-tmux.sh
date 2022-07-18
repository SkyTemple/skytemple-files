#!/usr/bin/env bash

# Runs all tests:
#  1. Non ROM-tests Python implementation
#  2. Non ROM-tests Rust implementation
#  3. ROM-tests Python implementation
#  4. ROM-tests Rust implementation
#
# The tests a run in a new windows in the current
# tmux environment. The window is split into four
# panes with each of the pane running one of the tests.
#
# The first argument is the path to the ROM.
#
# A second argument can be passed in, it will be run 
# before each test is executed in each pane.
# 
# The command defaults to: "source ~/.virtualenvs/skytemple/bin/activate"

rom_path=$1
cmd=${2:-"source ~/.virtualenvs/skytemple/bin/activate"}

cd test
# the sleeps are so the resize happens before pytest launches
tmux new-window "$cmd && sleep 1 && SKYTEMPLE_TEST_ROM=$rom_path SKYTEMPLE_USE_NATIVE=1 pytest -m romtest -n 2; echo 'Press enter to exit'; read"
tmux split-window "$cmd && sleep 1 && SKYTEMPLE_TEST_ROM=$rom_path pytest -m romtest -n 2; echo 'Press enter to exit'; read"
tmux split-window "$cmd && sleep 1 && SKYTEMPLE_USE_NATIVE=1 pytest -m 'not romtest' -n 2; echo 'Press enter to exit'; read"
tmux split-window "$cmd && sleep 1 && pytest -m 'not romtest' -n 2; echo 'Press enter to exit'; read"
tmux select-layout tiled
