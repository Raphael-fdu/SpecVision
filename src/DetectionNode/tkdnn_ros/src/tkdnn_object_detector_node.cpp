/* 
tkdnn_object_detector_node.cpp

Created on: 2020/09/30
Author: Hiroaki Kubo
Institute: Global Walkers
*/

#include <iostream>
#include <vector>
#include <signal.h>
#include <stdlib.h>
#include <string>
#include <unistd.h>
#include <mutex>
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
//#include <node_handle.h>

#include "CenternetDetection.h"
#include "MobilenetDetection.h"
#include "Yolo3Detection.h"

//message headers
#include <tkdnn_ros/bbox.h>
#include <tkdnn_ros/batchBbox.h>

static const std::string OUTPUT = "Output";
static bool gRun = true;

void sig_handler(int signo)
{
    std::cout << "request gateway stop\n";
    gRun = false;
}

class TKDNN_DETECTION
{
private:
    ros::NodeHandle nh_; //定义ROS句柄
    image_transport::ImageTransport it_;
    image_transport::Subscriber image_sub_;
    image_transport::Subscriber image_sub_2_;

    ros::Publisher bbox_pub;
    ros::Publisher bbox_pub_2;

    std::string weightsModel;
    std::vector<cv::Mat> batch_frame;
    std::vector<cv::Mat> batch_dnn_input;

    int numClasses;
    int n_batch = 1;
    float conf_thresh = 0.5;

    tk::dnn::DetectionNN *detNN;
    tk::dnn::Yolo3Detection yolo;

public:
    TKDNN_DETECTION() : it_(nh_) //构造函数
    {
        image_sub_ = it_.subscribe("/euresys_cam/image_color", 1, &TKDNN_DETECTION::detect_callback, this);
        bbox_pub = nh_.advertise<tkdnn_ros::batchBbox>("/tkDNN_ros/batchBbox", 1);
        //download weightsModel from the parameter server
        nh_.getParam("yolo_model/weights_file/name", weightsModel);
        nh_.getParam("yolo_model/detection_classes/value", numClasses);
        detNN = &yolo;
        detNN->init(weightsModel, numClasses, n_batch, conf_thresh);
        cv::namedWindow(OUTPUT);
    }
    ~TKDNN_DETECTION() //析构函数
    {
        cv::destroyWindow(OUTPUT);
    }
    void detect_callback(const sensor_msgs::ImageConstPtr &msg)
    {
        cv_bridge::CvImagePtr cv_ptr; //声明一个CvImage指针的实例
        try
        {
            cv_ptr = cv_bridge::toCvCopy(msg);
        }
        catch (cv_bridge::Exception &e)
        {
            ROS_ERROR("cv_bridge exception: %s", e.what());
            return;
        }

        image_process(cv_ptr->image, msg);
    }
    /*
        这是tkDNN目标检测的主要函数，生成检测框并显示在opencv窗口上。
    */
    void image_process(cv::Mat img, const sensor_msgs::ImageConstPtr &msg)
    {
        batch_dnn_input.clear();
        batch_frame.clear();

        std::string frame_id = msg->header.frame_id;

        tk::dnn::box b;
        int x0, w, x1, y0, h, y1, cl;

        tkdnn_ros::bbox bbox;
        tkdnn_ros::batchBbox *batchBbox = new tkdnn_ros::batchBbox;

        for (int bi = 0; bi < n_batch; ++bi)
        {
            batch_frame.push_back(img);
            batch_dnn_input.push_back(img.clone());
        }
        ros::Time begin = ros::Time::now();
        detNN->update(batch_dnn_input, n_batch);
        ros::Time end = ros::Time::now();

        for (int bi = 0; bi < n_batch; ++bi)
        {
            sensor_msgs::ImagePtr msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", img).toImageMsg();
            batchBbox->batchBbox.clear();
            uint64_t latency = (end.toNSec() - begin.toNSec()) / 1000000;
            batchBbox->latency = latency;

            batchBbox->img_processed = *msg;
            batchBbox->img_processed.header.frame_id = frame_id;
            for (int i = 0; i < detNN->batchDetected[bi].size(); i++)
            {
                b = detNN->batchDetected[bi][i];
                x0 = b.x;
                x1 = b.x + b.w;
                y0 = b.y;
                y1 = b.y + b.h;
                cl = b.cl;
                bbox.x0 = x0;
                bbox.x1 = x1;
                bbox.y0 = y0;
                bbox.y1 = y1;
                bbox.cl = cl;
                if (cl == 0)
                {
                    batchBbox->batchBbox.push_back(bbox);
                }
            }

            if (ros::ok())
            {
                bbox_pub.publish(*batchBbox);
                // ros::spinOnce();
                delete batchBbox;
            }
        }
    }
};

int main(int argc, char **argv)
{
    ros::init(argc, argv, "tkdnn_ros");
    signal(SIGINT, sig_handler);

    // Path to weights file
    // nh.getParam("yolo_model/weights_file/name", weightsModel);
    // std::cout << "weightsModel: " << weightsModel << std::endl;

    // // get class size
    // nh.getParam("yolo_model/detection_classes/value", numClasses);
    // std::cout << "num_classes: " << numClasses << std::endl;
    TKDNN_DETECTION obj;

    ros::spin();
    return 0;
}
