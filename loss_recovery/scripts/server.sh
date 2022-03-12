#!/bin/bash

mkdir /tmp/quic-data
cd /tmp/quic-data
wget -p --save-headers https://www.example.org

cd /home/qibao/chromium/src
./out/Default/quic_server --quic_response_cache_dir=/tmp/quic-data/www.example.org --certificate_file=net/tools/quic/certs/out/leaf_cert.pem --key_file=net/tools/quic/certs/out/leaf_cert.pkcs8
