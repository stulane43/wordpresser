#!/bin/bash

pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}

pushd .
cd $2
webhost=$(echo "$1" | awk -F/ '{print $1$3}' | sed s/:/_/g)
echo $1
wpscan --http-auth $3 --disable-tls-checks --request-timeout 4 --connect-timeout 4 --url $1 -f json -o $webhost.discover.wp.json
popd