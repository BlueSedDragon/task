#!/bin/bash

ROOT='/tmp/code/'
NAME=$1
DIR=$ROOT'/'$NAME

mkdir $DIR || {
	echo 'mkdir failed '$?
	exit 1
}

cd $DIR
apt source $NAME --download-only || {
	echo 'apt failed '$?
	exit 2
}

