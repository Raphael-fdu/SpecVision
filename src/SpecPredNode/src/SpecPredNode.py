import numpy as np
import torch
import torchvision.transforms as transforms

import cv2
import rospy
import PIL

from utils import *
from tkdnn_ros.msg import batchBbox
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32MultiArray



class SpecPred:
    def __init__(self, use_cuda):
        rospy.init_node("SpecPred")
        
        self.pub = rospy.Publisher("/SpecPred/spectrum", Float32MultiArray,1)
        self.sub = rospy.Subscriber("/tkDNN_ros/batchBbox", Float32MultiArray,self.callback)
        self.transform = transforms.Compose([transforms.Resize([224, 224]),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.0943, 0.0428, 0.1029], std=[0.4348, 0.3602, 0.1520])])
        self.use_cuda = use_cuda
        self.model = torch.load("test_model.pth")
    
    def infer(self,model, x):
        model.eval()
        s = model(x)
        return s
    
    def callback(self, batchBbox):
        bridge = CvBridge()
        s = Float32MultiArray()
        img = bridge.imgmsg_to_cv2(batchBbox.img_processed)
        if len(batchBbox.batchBbox) != 0:
            bbox = batchBbox.batchBbox[-1]
            if bbox.x0 > 720 and bbox.x1 < 1200 and bbox.y0 > 200 and bbox.y1 < 800:
                # first convert BGR to RGB so that cv2 image
                # could be correctly converted to PIL
                bbox = cv2.cvtColor(
                    img[bbox.y0:bbox.y1, bbox.x0:bbox.x1], cv2.COLOR_BGR2RGB)

                # convert cv2 array to PIL images (to be made available for torch.transform)
                bbox = PIL.Image.fromarray(bbox)
                x = self.transform(bbox).view(1, 3, 224, 224)
                if self.use_cuda:
                    x = x.cuda()
                s.data = self.infer(self.model, x).data.cpu().numpy().to_list()
                self.pub.publish(s)
    
    def run(self):
        rospy.spin()
            
if __name__ == "__main__":
    use_cuda = torch.cuda.is_available()
    predictor = SpecPred(use_cuda)
    predictor.run()
    
    
    
