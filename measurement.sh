#!/bin/bash

if [ '$1' == 'large' ]; then
	FILE="/largefiles/1GB.zip"
fi

if [ '$1' == 'small' ]; then
	FILE="/img/1.jpg"
fi

TESTNAME=$2

FORMAT="\nhttp_code: %{http_code}\nremote_ip: %{remote_ip}\nsize_download: %{size_download}\nspeed_download: %{speed_download}\ntime_connect: %{time_connect}s\ntime_namelookup: %{time_namelookup}s\ntime_pretransfer: %{time_pretransfer}s\ntime_starttransfer: %{time_starttransfer}s\ntime_redirect: %{time_redirect}s\ntime_total: %{time_total}s\n"

END=100

mkdir -p ./results_$TESTNAME/redirect
mkdir -p ./results_$TESTNAME/noredirect

for i in $(seq 1 $END); do
	echo "Measurement $i"
	curl -L -o /dev/null -svkw "$FORMAT"  http://cdn.dizp.bt:8080/assets$FILE > ./results_$TESTNAME/redirect/largefile_$i.txt
	sleep 0.1
	curl -L -o /dev/null -svkw "$FORMAT"  http://cdn.dizp.bt:8082/assets$FILE > ./results_$TESTNAME/noredirect/largefile_$i.txt
	sleep 0.1
done

