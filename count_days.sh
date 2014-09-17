#!/bin/bash

if [ $# -ne 2 ]
then
    echo "Usage: $0 <start> <end>"
	echo "Both <start> and <end> are integers in YYYYMMDD format, e.g. 20141901"
	exit
fi

for shift in AM PM Snack
do
	echo $shift: `redis-cli ZRANGEBYSCORE slotsbydate $1 $2 | grep $shift | wc -l`
done	
