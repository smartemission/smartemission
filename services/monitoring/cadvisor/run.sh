#!/bin/bash
#
export PARENT_HOST=`ip route show | grep docker0 | awk '{print \$9}'`
export GOROOT="/usr/lib/go-1.9"
export GOPATH="/opt/cadvisor/src/github.com/google/cadvisor"
export PATH="${GOPATH}:${GOROOT}/bin:${PATH}"

cd ${GOPATH}
./cadvisor -listen_ip ${PARENT_HOST} -port 8080
