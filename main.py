#! /usr/bin/env python
# coding=utf-8
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def doMsg(msg):
    rospy.loginfo("I heard:%s", msg.data)

# def callback(data):
#     imgdata = CvBridge().imgmsg_to_cv2(data, "rgb8")
#     cv2.imwrite("/home/eaibot/cam_test.jpg", imgdata)

def listener():
    rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("/usb_cam/image_correct", Image, callback)
    img_data = rospy.wait_for_message("/usb_cam/image_correct", Image, timeout=10)
    imgdata = CvBridge().imgmsg_to_cv2(img_data, "rgb8")
    imgdata = imgdata[:, :, ::-1]
    cv2.imwrite("/home/eaibot/cam_test.jpg", imgdata)

if __name__ == "__main__":
    listener()
    rospy.spin()
