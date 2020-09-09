#!/bin/bash

# Bash script for Scanning WiFi Access Points and recording Quality and Signal Strength (RSSI)
# Author: Alex Brown

if [ -z "$1" ]
then
	echo "You need to specify the wireless interface to use. Select from below.";
	iwconfig;
	exit 1;
fi

if [ -z "$2" ]
then
	echo "Need to specify a AP ESSID to listen for";
	exit 1;
fi

if [ -z "$3" ]
then
	echo "Need to specify an output file";
	exit 1;
fi

WAIT_TIME=5;
INTERFACE=$1;
ESSID=$2;
OUT_FILE=$3;

echo "time,BSSID,Quality,RSSI,ESSID" > ${OUT_FILE};

while :;
do

	result=$(sudo iwlist ${INTERFACE} scanning | 
		grep -E "Cell|Quality|Last Beacon|ESSID" | 
		sed -e "s/^[ \t]*//" -e "s/[ \t]*$//" | 
		sed -e "s/Quality=//" -e "s/Signal level=// " -e "s/ESSID://" -e "s/ dBm//" -e "s/  / /" |
		awk '{ORS = (NR % 3 == 0)? "\n" : " "; print}' |
		cut -c 20- |
		csvformat -d ' ' -D ',' |
		grep -e "${ESSID}");

	exe_time=$(date +'%y-%m-%d-%H-%M-%S')	
	
	for line in ${result};
	do
		echo "${exe_time},${line}" | tee -a ${OUT_FILE};
	done
	sleep ${WAIT_TIME};
done	
