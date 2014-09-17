#!/bin/bash

if [ $# -ne 2 ]
then
    echo 'Usage: count_days.sh <start> <end>'
	echo 'Both <start> and <end> are integers in YYYYMMDD format, e.g. 20141901'
	exit
fi

START=$1
END=$2

for shift in AM PM Snack
do
	echo $shift: `redis-cli ZRANGEBYSCORE slotsbydate $START $END | grep $shift | wc -l`
done	
