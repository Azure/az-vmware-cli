#!/bin/sh -e
npm install -g autorest
npm install -g oav --unsafe-perm=true --allow-root
apt-get update
apt-get install libunwind-dev -y