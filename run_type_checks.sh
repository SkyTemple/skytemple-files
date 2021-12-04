#!/usr/bin/env sh
# Runs mypy checks for all projects that support it
# Assumes the following file structure:
# ..
#  -> .
#  -> skytemple_rust
#  -> skytemple
#  -> ssb_debugger
#  -> randomizer

echo "skytemple-files"
echo "==============="
mypy --config-file mypy.ini

cd ../explorerscript
echo "explorerscript"
echo "=============="
mypy --config-file mypy.ini

cd ../skytemple_rust
echo "skytemple-rust"
echo "=============="
mypy --config-file mypy.ini

cd ../randomizer
echo "skytemple-randomizer"
echo "===================="
mypy --config-file mypy.ini

cd ../ssb_debugger
echo "skytemple-ssb-debugger"
echo "======================"
mypy --config-file mypy.ini

cd ../skytemple
echo "skytemple"
echo "========="
mypy --config-file mypy.ini
