#!/bin/sh

PYTHON=python3.11

cd "${BASH_SOURCE%/*}/" || exit

rm -fr env
$PYTHON -m venv env
source env/bin/activate
pip install --upgrade pip
pip install pyrsistent networkx numpy matplotlib

