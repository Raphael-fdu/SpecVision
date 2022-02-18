#! /bin/bash

DATACMTX_ROOT="/home/chemcello/Projects/The-PC-Pixel-Project/data/testSet_confusionMat"
TESTCMTX_ROOT="/home/chemcello/Projects/The-PC-Pixel-Project/plotting/Ch2_ObjDetection/1_confusion_mtx"


if [ $1 ]
then
	# do infer
	ROOT=`dirname $0`
	$ROOT/darknet -i 1 detector test $ROOT/data/droplet_capillary.data $ROOT/cfg/yolov4-tiny-droplet-quaternary.cfg $1 -thresh 0.50 -dont_show -save_labels < $DATACMTX_ROOT/test.txt
else
	echo "Error: miss infer model"
fi

