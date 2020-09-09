#!/bin/bash

if [ -z "$1" ]
then
	echo "Need a wifi interface to listen to! Network interfaces with wireless capability shown below.";
	iwconfig;
	exit 1;
fi

if [ -z "$2" ]
then
	echo "Need to specify the ESSID of the WiFi AP to listen for"
	exit 1;
fi


INTERFACE=$1
ESSID=$2

if [ -z "$3" ]
then
	OUTPUT_FILE="${ESSID}-$(date +'%y-%m-%d-%H-%M-%S')"
else
	OUTPUT_FILE=$1
fi

sudo airmon-ng start "${INTERFACE}";
sudo airodump-ng -I 10 -w "${OUTPUT_FILE}" --output-format csv -N "${ESSID}" "${INTERFACE}";
