#!/bin/bash
#
# Init the STA DB using REST. USE WITH CARE! IT DELETES ALL HISTORY OF STA PUBLICATION!
#
# NB  NOT USED, kept for ref, for GOST use db-init-gost.sh !!
SCRIPT_DIR=${0%/*}

pushd ${SCRIPT_DIR}/../
. common.sh
popd

python staclear.py $sta_host $sta_port  $sta_path $sta_user $sta_password
