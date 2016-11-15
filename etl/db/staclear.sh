#!/bin/bash
#
# Init the STA DB using REST. USE WITH CARE! IT DELETES ALL HISTORY OF STA PUBLICATION!
#
. ../options/nusa.args
python staclear.py $sta_host $sta_port $sta_user $sta_password
