# coding=utf-8
import os
import time

import rospy

from std_msgs.msg import String


def start_ocr(data):
    print("收到开始信号")
    if data != "":
        print("correct")
        os.system('python2 ./get_img.py')
        time.sleep(2)
        os.system('python ./predict_backup_2.py')  # 运行识别程序
        time.sleep(3)
        f = open("./result.txt", "r")
        result_str = f.read()
        print(result_str)
        result_pub = rospy.Publisher('ocr_result', String, queue_size=1)
        time.sleep(3)
        rate = rospy.Rate(100)  # 100hz
        result_pub.publish(result_str)
        rate.sleep()
    else:
        print("error")


def init_pub():
    global result_pub
    result_pub = rospy.Publisher('ocr_result', String, queue_size=1)
    print("初始化完毕")


if __name__ == '__main__':
    # 建立节点
    rospy.init_node('VM_main_node', anonymous=True)
    time.sleep(6)
    init_pub()
    # 订阅话题
    time.sleep(6)
    sub = rospy.Subscriber('start_ocr', String, start_ocr)
    print("开始监听start_ocr")
    # 调用回调函数，并阻塞，直到程序结束
    rospy.spin()
