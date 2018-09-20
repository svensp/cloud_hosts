#!/bin/sh
apt-get update
while ! apt-get -y install python ; do
	echo "Failed to install python, waiting 5s"
	sleep 5s
done
