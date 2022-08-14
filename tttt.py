import rospy
from sensor_msgs.msg import Image


def listener():
    rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("/usb_cam/image_correct", Image, callback)
    img_data = rospy.wait_for_message("/usb_cam/image_raw", Image, timeout=10)
    print(img_data)


if __name__ == '__main__':
    listener()
