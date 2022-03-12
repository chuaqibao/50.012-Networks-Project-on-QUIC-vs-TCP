/bin/bash

mkdir -p raw processed plt tmp

sudo ifconfig lo mtu 1500
sudo sysctl -w net.ipv6.conf.lo.disable_ipv6=1

/home/qibao/chromium/src/out/Default/quic_server --quic_response_cache_dir=/var/www/html –certificate_file=/home/qibao/chromium/src/net/tools/quic/certs/out/leaf_cert.pem –key_file=/home/qibao/chromium/src/net/tools/quic/certs/out/leaf_cert.pkcs8
