#!/bin/bash
#
# Init GOST and publication shorthand.
#

SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}/../
./db-init-gost.sh
popd


./sta-publisher-init.sh
