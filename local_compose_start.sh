#!/bin/bash

if [ -z "$1" ]
  then
    echo "No user supplied"
    exit 1
fi

USER=$1

kinit -c ./krb5_tgt $USER@MPT.INTRA                                                                    

ktutil <<EOF                 
addent -password -p $USER@MPT.INTRA -k 1 -e aes256-cts-hmac-sha1-96
# You'll be prompted for password
wkt ./krb5.keytab
quit
EOF

# Read and escape the YAML content
export CONF_REPO_CONTENT=$(cat conf_repo.yaml | python3 -c 'import sys, json; print(json.dumps(sys.stdin.read()))')

docker-compose up --build --remove-orphans