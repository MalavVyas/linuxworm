#!/bin/sh
FILE=/tmp/client.py
if [ ! -f "$FILE" ]; then
	echo "$FILE does not exist."
	wget "http://192.168.5.20/client.py" -P /tmp
	chmod +x /tmp/client.py
fi
python3 /tmp/client.py 192.168.5.20 $(echo $(ip a | grep ens160 | grep "inet " | cut -d " " -f6 | cut -d "/" -f1)/$(uname -a | cut -d " " -f2))

