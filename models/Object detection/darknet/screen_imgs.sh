#! /bin/bash

TEST_ROOT="/home/chemcello/Projects/The-PC-Pixel-Project/utils/camera_stream_record"

if [ $1 ]
then
	# do infer
	ROOT=`dirname $0`
	./darknet -i 1 detector test $ROOT/data/droplet_capillary.data $ROOT/cfg/yolov4-tiny-droplet-quaternary.cfg $1 -thresh 0.50 -dont_show -save_labels < $TEST_ROOT/test.txt
else
	echo "Error: miss infer model"
fi

