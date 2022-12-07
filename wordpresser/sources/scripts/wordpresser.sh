#!/bin/bash

pushd () {
    command pushd "$@" > /dev/null
}
popd () {
    command popd "$@" > /dev/null
}

amass () {
    pushd .
    cd wordpresser/out
    docker run -v /Users/slane/prh/tools/wordpresser/wordpresser/out/amass:/.config/amass/ caffix/amass intel -d penguinrandomhouse.com -whois
    mv amass/amass.txt .
    popd
}

httprobe () {
    pushd .
    cd wordpresser/out
    cat wmap.out cycognito.out amass.txt terminus.out | sort -u > discovered_hosts.out
    grep -v -f wordpresser.out discovered_hosts.out  > discovered_hosts_new.out
    cat discovered_hosts_new.out | ~/go/bin/httprobe --prefer-https -c 50 > webhosts.txt
    popd
}

wpscan_basicauth_required() {
    pushd .
    cd wordpresser/out/wpscan
    for i in $(grep -l "HTTP authentication required" ./*);
    do 
        echo $(cat $i | jq '.target_url' | sed 's/\"//g' | sort -u) > ../tmp_basic_auth_required.out
    done
    cat ../tmp_basic_auth_required.out | sort -u > ../basic_auth_required.out
    rm -f ../tmp_basic_auth_required.out
    popd
}

wpscan_redirects() {
    pushd .
    cd wordpresser/out/wpscan
    for i in $(grep -l "but does not seem to be running WordPress" ./*);
    do 
        echo $(cat $i | jq '.target_url' | sed 's/\"//g' | sort -u) >> ../notWordpress.out
    done
    grep -l "but does not seem to be running WordPress" ./* | xargs rm
    for i in $(grep -l "The URL supplied redirects to" ./*);
    do 
        redirect=$(cat $i | jq '.scan_aborted' | sed -n 's/.*redirects to //;s/\S*[.] Use the.*//;p;')
        echo "$(cat $i | jq '.target_url' | sed 's/\"//g' | sort -u) - $redirect" >> ../og_redirects.out
    done
    grep -l "The target is responding with a 403" ./* | xargs rm
    touch ../redirects.txt
    for i in $(grep -l "The URL supplied redirects to" ./*);
    do 
        echo $(cat $i | jq '.target_url' | sed 's/\"//g' | sort -u) >> ../redirects.out
    done
    grep -l scan_aborted ./* | xargs -I % sh -c 'r=$(sed -n '"'"'/scan_aborted/{s/.*redirects to //;s/\S*[.] Use the.*//;p;}'"'"' %); echo $r >> ../redirects.txt; '
    popd
}

wpscan_clean () {
    pushd .
    cd wordpresser/out/wpscan
    for i in $(grep -l scan_aborted ./*);
    do 
        echo $(cat $i | jq '.target_url' | sed 's/\"//g' | sort -u) >> ../scans_aborted.out
    done
    grep -l scan_aborted ./* | xargs rm
    cd ..
    for i in $(cat wpscan/*.discover.wp.json | jq '.target_url' | sed 's/\"//g' | sort -u); 
    do 
        echo $i >> tmp_wpscan.out
    done
    cat tmp_wpscan.out | sort -u > wpscan.out
    rm -f tmp_wpscan.out
    popd
}

case "$1" in
        amass)
                amass
                ;;
        httprobe)
                httprobe
                ;;
        wpscan_basicauth_required)
                wpscan_basicauth_required
                ;;
        wpscan_redirects)
                wpscan_redirects
                ;;
        wpscan_clean)
                wpscan_clean
                ;;
        *)
                echo "Usage: $0 {amass|httprobe|wpscan_redirects|wpscan_clean}"
                echo ""
                echo "Use this shell script to run wordpresser functions."
esac