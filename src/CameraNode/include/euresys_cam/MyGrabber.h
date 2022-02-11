#include <EGrabber.h>
#include <FormatConverter.h>
#include <image_transport/image_transport.h>
#include <camera_info_manager/camera_info_manager.h>

using namespace Euresys;
class MyGrabber : public EGrabber<CallbackMultiThread>
{
public:
    MyGrabber(EGenTL &gentl);
    ~MyGrabber()
    {
        stop();
        shutdown();
    }

    sensor_msgs::Image image_;
    FormatConverter converter;

private:
    const size_t width = 1920;
    const size_t height = 1080;
    const size_t imgSize = 2073600;
    const size_t imgPitch = 1920;
    const std::string format = "BayerGR8";
    ros::NodeHandle nh_;
    image_transport::Publisher pub_;
    uint8_t *img_;

    virtual void onNewBufferEvent(const NewBufferData &data) override;
};

MyGrabber::MyGrabber(EGenTL &gentl) : EGrabber<CallbackMultiThread>(gentl), converter(gentl)
{
    setInteger<DeviceModule>("EventNotificationAll", true);
    setInteger<StreamModule>("EventNotificationAll", true);
    setInteger<InterfaceModule>("EventNotificationAll", true);

    setString<RemoteModule>("PixelFormat", "BayerGR8");
    // setInteger<RemoteModule>("Width",1440);
    // setInteger<RemoteModule>("Height",900);

    enableEvent<NewBufferData>();
    reallocBuffers(20);

    // ROS publishing topic
    image_transport::ImageTransport it(nh_);
    pub_ = it.advertise("/euresys_cam/image_color", 1);

    // Image data
    image_.height = height;
    image_.width = width;
    image_.step = width * 3;
    image_.encoding = "bgr8";
    image_.data.resize(image_.height * image_.step);
}

void MyGrabber::onNewBufferEvent(const NewBufferData &data)
{
    ScopedBuffer buf(*this, data);

    // Obtain frame ID and the image pointer
    uint64_t frameID = buf.getInfo<uint64_t>(GenTL::BUFFER_INFO_FRAMEID);
    uint8_t *imgPtr = buf.getInfo<uint8_t *>(GenTL::BUFFER_INFO_BASE);

    image_.header.frame_id = std::to_string(frameID);

    // Convert the image from Bayer format to RGB 
    FormatConverter::Auto bgr(converter, FormatConverter::OutputFormat("BGR8"), 
                                    imgPtr, format, width, height, imgSize, imgPitch);

    memcpy((uint8_t *)(&image_.data[0]), bgr.getBuffer(), image_.step * image_.height);
    ros::Time now = ros::Time::now();
    image_.header.stamp = now;
    pub_.publish(image_);
}
