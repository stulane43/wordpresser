#!/bin/bash

get_plugins () {
SiteEnv="${sitename}.${env}"
domains=`terminus domain:list $SiteEnv --fields id --format=list`
for domain in $domains
do
	if [[ $domain =~ ^(www\.)|io ]]; then
		:
	else
		if [[ $domain = 'timothysnyder.org' ]] || [[ $domain = 'robertcaro.com' ]] || [[ $domain = 'penguinrandomhouse.ca' ]] || [[ $domain = 'stage.penguinrandomhouse.ca' ]] || [[ $domain = 'dev.penguinrandomhouse.ca' ]] || [[ $domain = 'dev.theloraxproject.com' ]] || [[ $domain = 'knopfdoubleday.com' ]]; then
			echo 'skipping' $domain
		elif grep -Fxq "$domain" wordpresser.out; then
			echo 'skipping' $domain '- recently scanned'
		else
			echo $domain >> terminus.out
			for plugin in `terminus wp $SiteEnv -- plugin list --format=csv`
			do
				echo $domain, $plugin >> plugins.csv
			done
		fi
	fi
done
}

pushd .
cd wordpresser/out
for sitename in `terminus org:site:list "Penguin Random House" --field=name`
do
	env=$1
	get_plugins
done
popd