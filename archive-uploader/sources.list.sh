#!/bin/bash
TIME=`date +%s` || {
	echo 'get time failed '$?
	exit 1
}

cp /etc/apt/sources.list '/etc/apt/sources.list.'$TIME'.bak' || {
	echo 'cp backup failed '$?
	exit 2
}
cp ./sources.list /etc/apt/sources.list || {
	echo 'cp override failed '$?
	exit 3
}

