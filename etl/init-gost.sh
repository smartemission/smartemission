#!/usr/bin/env bash
pushd db
./db-init-gost.sh
./sta-publisher-init.sh
popd

pushd ../services/gost
./run.sh
popd
