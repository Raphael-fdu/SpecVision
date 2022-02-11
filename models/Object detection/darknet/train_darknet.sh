#! /bin/bash

# if training with multi gpu, first train on 1 GPU for like 1000 iterations,
# then train with multigpu by passing and arg to this shell script


ROOT=/home/chemcello/Softwares/darknet-master
RESULTS_FOLDER=$ROOT/results/`date +%Y-%m-%d-%H:%M:%S`
export DISPLAY=:1

# first create folders to store the training results
if [ ! -s "$RESULTS_FOLDER" ]
then 
	mkdir -p $RESULTS_FOLDER
	mkdir -p $RESULTS_FOLDER/backup
fi

# rewrite the .data file and specify the saving locations for the models
sed -i "5c backup = $RESULTS_FOLDER/backup/" $ROOT/data/droplet_capillary.data 

# put a commentary file (by default, $1)  into the results folder
echo $1 > $RESULTS_FOLDER/description.txt



starttime=`date +%s`

# Use two GPUs for training, and use the original_quaternary model as the starting point
$ROOT/darknet detector train $ROOT/data/droplet_capillary.data $ROOT/cfg/yolov4-tiny-droplet-quaternary.cfg $ROOT/pretrained_models/yolov4-tiny.conv.29 -gpus 0,1 -map > $RESULTS_FOLDER/output.txt

endtime=`date +%s`
c=`expr $endtime - $starttime`

echo $c > $RESULTS_FOLDER/time.txt

#else
#	$ROOT/darknet detector train $ROOT/data/droplet_capillary.data $ROOT/cfg/yolov4-tiny-droplet-quaternary.cfg $ROOT/backup/yolov4-tiny-droplet-quaternary_1000.weights -gpus 0,1 -map
#fi
 
