#include <euresys_cam/MyGrabber.h>


using namespace Euresys;
using namespace EURESYS_NAMESPACE;

int main(int argc, char** argv)
{
    ros::init(argc,argv,"euresys_cam_node");
    EGenTL gentl;
    MyGrabber  mygrabber(gentl);
    mygrabber.start();
    ros::spin();
}