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
wpscan --disable-tls-checks --url $1 --api-token $3 -f json -o $webhost.vulns.wp.json
popd