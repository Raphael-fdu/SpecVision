# Models



## Dependencies

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



## Object Detection

Object Detection dependends on two open-source packages including [**darknet**](https://github.com/AlexeyAB) and [**tkDNN**](https://github.com/ceccocats/tkDNN). **Darknet** is a framework designed for optimized implementation of popular object detection algorithms in C. In this repository we use darknet primarily for training. **tkDNN** is a high-performance library for TensorRT accelerated inference of object detection networks. Using tkDNN to detect custom objects require some extra toggling of the source code therefore the one used in our repository is slightly different than the official branch. 

Both libraries require compilation before use. Here is a simplified guide of how you may compile those two libraries for your own use.

### How to compile

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

   

### Training

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



### Export weights to tkDNN

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

   

## Spectrum Prediction

The spectrum prediction networks is based on pytorch. Spectra data needs to be preprocessed using the following python package so make sure they are properly installed in your system.

```shell
pip3 install BaselinRemoval
pip3 install scipy
```



### How to train

1. Go to `config` and set training epoachs and learning rate as well as data paths in config.yaml

2. (optional) If you are planing to perform transfer learning, prepare your pre-trained model and make proper changes in the code `train_transfer_learning.py`

3. Run the training program in the commandline.

   `python3 train_from_scratch.py <# of trial> <comment>`

   



