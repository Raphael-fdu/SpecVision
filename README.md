# SpecVision

Author: Xucheng (Raphael) Zhang

## Intro

Specvision is a reconfigurable framework for automating optical analysis in microfludics with machine vision techniques. In its current form, we integrate an image-to-spectrum prediction network with a droplet detection algorithm to achieve sub-milisecond spectral readout in real time.

The entire software is built on top of an open-source robotic framework named **Robot Operating System (ROS)** (https://www.ros.org), in pursuit of flexibility. With the help of **ROS**, we are able to separate our functionalities into independent **Nodes** that can be modified or replaced with ease, freeing developers from the need of rebuilding the entire project. This decoupling strategy also allows for extra space for the expansion of the system's functionality e.g. intelligent decision making, as we deem our project as half-way towards a fully closed-loop self-driving laboratory.



## Prerequisite

* Ubuntu 18.04
* Robot Operating System (ROS) melodic
* TensorRT 7.2.0 (or >= 5)
* OpenCV 4.5.2 (or >= 4)
* cmake 3.20 (or >= 3.15)
* CUDA 11.0 (>= 10.0)
* pytorch 1.8.1
* pySide 2



## Overview 

```
.
├── build
├── devel
├── src
│   ├── CameraNode
│   ├── DetectionNode
│   ├── SpecPredNode
│		├── PivotNode
│		└── PumpControl
├── training codes
│   ├── Object detection
│   └── Spectrum prediction
└── Readme.md
```



* CameraNode

  This node handles camera control and streaming. In this node we gain access to the camera driver as well as the framegrabber SDK. By tunnelling the image from the framegrabber to our ROS interface in the form of a "topic" the RGB pixel information is made accessible to all other nodes subscribing to it.

  

* DetectionNode

  This node hosts the object detection functionality enabled by the open-source library called tkDNN. tkDNN makes use of a hard-ware level acceleration named tensorRT offered by nVidia GPUs and delivers sub-millisecond inferrence computing a light-weight model YOLOv4-Tiny.

  

* SpecPredNode

  This node uses a convolutional neural network to map the droplet image of a photonic crystal material into its reflection spectrum, which is conventionally collected using a standalone spectrometer. But now with the power of AI, we can directly compute it out simply using the optical image.



* PivotNode

  This is the central node where all information needed for display is collected and sent to a graphic user interface. By taking advantage of the threading functionality offered by the PySide2 (Qt for Python, https://doc.qt.io/qtforpython/), a user-friendly interface is made possible with the following features:

  * Real time monitoring of the camera streaming, with detected droplets annotated.

  * Real time readout of the predicted spectrum.

  * Toggling of the pump rate (or on/off switch)

  * Camera control

    

## How to use

Make sure all prerequisites are properly installed.

* Compilation

1. Replace the CameraNode to the one suited for your own imaging system.

2. Go to the root directory of this repository and type the following:

   ```
   catkin_make
   ```

   If it compiles with no errors popping up, you are good to go!



* Running

1. Open up a terminal, and type in:

   ```shell
   roscore
   ```

   This will call up a base process which is a prerequisite for all other nodes to run.

2. Run CameraNode

   This may vary for different users as people use cameras of varied brands and models. 

   In our case, it looks like this:

   ```
   rosrun CameraNode euresys_cam
   ```

   where `rosrun` is an ros command for running a node. `CameraNode` is the name of the package and `euresys_cam` is the name of the executable. Our system uses an Euresys frame grabber so we named it accordingly.

3. Run DetectionNode

   Before you run the detection node, you may want to change the configuration file so to specify your own .rt engine.

   Go to `DetectionNode/tkdnn_ros/config/tkdnn.yaml` and specify the path of the .rt engine in the `weights_file` attribute.

   Then run the following code

   `roslaunch DetectionNode tkdnn_ros.launch`

   This will call up a launch file and store the information in the config file into a parameter server which would be accessed during runtime of the detection algorithm.

4. Run PivotNode

   ```shell
   rosrun PivotNode pivot.py
   ```

   

## Training of the models



### Dependencies

* CUDA 11.0 (or >= 10.0)
* cuDNN 8.04  (or >= 7.3)
* TensorRT 7.2.0 (or >= 5)
* OpenCV 4.5.2 (or >= 4)
* cmake 3.20 (or >= 3.15)
* yaml-cpp 0.5.2
* Eigen3 3.34
* curl 7.58
* pytorch 1.8.1
* Some other common python packages including numpy, pandas, scipy, etc.



### Object Detection

Object Detection dependends on two open-source packages including [**darknet**](https://github.com/AlexeyAB) and [**tkDNN**](https://github.com/ceccocats/tkDNN). **Darknet** is a framework designed for optimized implementation of popular object detection algorithms in C. In this repository we use darknet primarily for training. **tkDNN** is a high-performance library for TensorRT accelerated inference of object detection networks. Using tkDNN to detect custom objects require some extra toggling of the source code therefore the one used in our repository is slightly different than the official branch. 

Both libraries require compilation before use. Here is a simplified guide of how you may compile those two libraries for your own use.

#### How to compile

For details and troubleshooting you may refer to the official github repositories by clicking the links above.

1. Make sure you have already installed all the dependencies listed above.

2. Compile darknet

   ```shell
   cd ./darknet/build
   cmake ..
   make -j[# of your CPU cores]
   ```

3. Compile tkDNN

   ```shell
   cd ./tkDNN/build
   cmake ..
   make -j[# of your CPU cores]
   ```

   

#### Training

Training is first done with darknet and then exporting the weight to tkDNN to compile the tensorRT engine.

1. Use [YOLO_MARK](https://github.com/AlexeyAB/Yolo_mark) to annotate the bounding boxes in your droplet images.
2. Go to ./darknet/cfg/ and modify the configuration file `yolov4-tiny-droplet.cfg`and make the following changes:
   * at each [ yolo ] layer, change the attribute `classes` to the number of classes in your detection task.
   * change `max_batches` to  change [`filters=255`] to filters=(classes + 5)x3 in the 3 `[convolutional]` before each `[yolo]` layer, keep in mind that it only has to be the last `[convolutional]`before each of the `[yolo]` layers
   * change line `max_batches` to (`classes*2000`, but not less than number of training images and not less than `6000`), f.e. [`max_batches=6000`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L20) if you train for 3 classes
   * change line `steps` to 80% and 90% of max_batches

3. Create file `obj.names` in the directory `build/darknet/x64/data/`, with objects names - each in new line
4. Create file `obj.data` in the directory `build/darknet/x64/data/`, containing (where **classes = number of objects**):
5. Put image-files (.jpg) of your objects in the directory `build/darknet/x64/data/obj/`
6. Create file `train.txt` in directory `build/darknet/x64/data/`, with filenames of your images, each filename in new line, with path relative to the executable `darknet`
7. Download pretrained model into `darknet/pretrained/models`
8. Start training by using the command line `./darknet detector train data/obj.data yolo-obj.cfg pretrained_models/yolov4.conv.29



#### Export weights to tkDNN

Weight export to tkDNN involves a different fork of darknet, which we include in the ./tkDNN folder as darknet_export

1. Go to tkDNN/darknet_export

2. Run the following commandline

   ```shell
   make
   mkdir layers debug
   ./darknet export <path-to-cfg-file> <path-to-weights> layers
   ```

   This will export the weight from the .path file into layers.

3. Go to `tkDNN/build/` and `mkdir yolov4-tiny-droplet`

4. Copy the two folders (layers and debug) into tkDNN/build/yolov4-tiny-droplet/

5. Run the executable `test_yolov4-tiny-droplet`

   If Succeeded, there will be a `.rt`file generated in the working directory.

   

### Spectrum Prediction

The spectrum prediction networks is based on pytorch. Spectra data needs to be preprocessed using the following python package so make sure they are properly installed in your system.

```shell
pip3 install BaselinRemoval
pip3 install scipy
```



#### How to train

1. Go to `config` and set training epoachs and learning rate as well as data paths in config.yaml

2. (optional) If you are planing to perform transfer learning, prepare your pre-trained model and make proper changes in the code `train_transfer_learning.py`

3. Run the training program in the commandline.

   `python3 train_from_scratch.py <# of trial> <comment>`

   

