# coding=utf-8
import os
import time

import rospy

from std_msgs.msg import String


def start_ocr(data):
    print("收到开始信号")
    if data == 'start_ocr':
        os.system('python /home/eaibot/aistudio/work/Ubuntu/predict_backup_2.py')  # 运行识别程序
        time.sleep(3)
        f = open("/home/eaibot/aistudio/work/Ubuntu/result.txt", "r")
        result_str = f.read()
        print(result_str)
        rate = rospy.Rate(100)  # 100hz
        result_pub.publish(result_str)
        rate.sleep()


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
    rospy.Subscriber('start_ocr', String, start_ocr)
    print("开始监听start_ocr")
    # 调用回调函数，并阻塞，直到程序结束
    rospy.spin()
