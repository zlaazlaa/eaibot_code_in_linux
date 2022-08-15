# coding=utf-8
import os
import select
import sys
import termios
import threading
import time
import tty
import rospy
from actionlib_msgs.msg import GoalID
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionResult
from std_msgs.msg import String
from dobot.srv import SetHOMECmd  # 调用回零话题
from dobot.srv import SetEndEffectorSuctionCup  # 调用末端回零话题
from dobot.srv import SetPTPCmd  # 调用机械臂点到点运动话题
from dashgo_tools.msg import check_msgActionResult

operation_keys = ['1', '2', '3', '4', 'k']

grap_up_x = 7
grap_up_y = -257
grap_up_z = 95
grap_up_r = -170

grap_down_x = 0
grap_down_y = 0
grap_down_z = -22
grap_down_r = -170

put_up_x = 7
put_up_y = 185
put_up_z = 67
put_up_r = 2

put_down_x = 7
put_down_y = 170
put_down_z = -29
put_down_r = 2

deliver_up_x = 7
deliver_up_y = -319
deliver_up_z = 25
deliver_up_r = -170

now_goal = '0'  # 记录当前导航目标点
desk_goal = 0  # 上次分拣台编号
node_list = []
dic = {'四川': 0, '安徽': 1, '湖南': 2, '广东': 3, '浙江': 4, '江苏': 5, '福建': 6, '河南': 7, 'none': 0}


class NodeCoordinate:
    def __init__(self, p_x, p_y, p_z, o_x, o_y, o_z, o_w):
        self.p_x = p_x
        self.p_y = p_y
        self.p_z = p_z
        self.o_x = o_x
        self.o_y = o_y
        self.o_z = o_z
        self.o_w = o_w


def send_goal(i):  # Go to point i
    global desk_goal
    desk_goal = int(i)
    global now_goal
    now_goal = i
    goal_msg = MoveBaseActionGoal()
    goal_msg.goal_id.id = i + '_' + str(time.time())
    i = int(i)
    goal_msg.goal.target_pose.pose.position.x = float(node_list[i].p_x)
    goal_msg.goal.target_pose.pose.position.y = float(node_list[i].p_y)
    goal_msg.goal.target_pose.pose.position.z = float(node_list[i].p_z)
    goal_msg.goal.target_pose.pose.orientation.x = float(node_list[i].o_x)
    goal_msg.goal.target_pose.pose.orientation.y = float(node_list[i].o_y)
    goal_msg.goal.target_pose.pose.orientation.z = float(node_list[i].o_z)
    goal_msg.goal.target_pose.pose.orientation.w = float(node_list[i].o_w)
    goal_msg.goal.target_pose.header.frame_id = 'map'
    # goal_msg.header.seq = int(time.time())
    goal_pub.publish(goal_msg)
    print("Going to:")


def main():
    init_listener()
    time.sleep(3)
    rospy.wait_for_service('DobotServer/SetHOMECmd')
    rospy.wait_for_service('DobotServer/SetPTPCmd')
    # t0 = rospy.Duration(5, 0)
    try:
        client = rospy.ServiceProxy('DobotServer/SetHOMECmd', SetHOMECmd)
        PTP_client = rospy.ServiceProxy('DobotServer/SetPTPCmd', SetPTPCmd)
        response = client()
        response = PTP_client(1, grap_up_x, grap_up_y, grap_up_z, grap_up_r)  # houmian,shangfang
    except rospy.ServiceException, e:
        print
        "Service call failed: %s" % e
    time.sleep(30)
    print (11111)
    # for i in ('8', '11'):
    #     send_goal(i)
    send_goal('8')


def nav_callback(data):
    print(data)
    if data.status.status == 3:
        goal_name = data.status.goal_id.id.split('_')[0]
        if goal_name >= '8':  # 到达分拣台
            print("到达分拣台")
            start_ocr_pub = rospy.Publisher('start_ocr', String, queue_size=10)  # 开始orc指令发布器
            time.sleep(3)
            start_ocr_pub.publish("start_ocr")
            ocr_result = rospy.wait_for_message('ocr_result', String, timeout=None)
            print("识别完毕")
            result = str(ocr_result).split('_')
            destination = result[0]
            x = int(result[1])
            y = int(result[2])
            # 机械臂抓取
            # TODO
            rospy.wait_for_service('DobotServer/SetEndEffectorSuctionCup')
            rospy.wait_for_service('DobotServer/SetPTPCmd')
            t1 = rospy.Duration(1, 0)
            try:
                end_client = rospy.ServiceProxy('DobotServer/SetEndEffectorSuctionCup', SetEndEffectorSuctionCup)
                PTP_client = rospy.ServiceProxy('DobotServer/SetPTPCmd', SetPTPCmd)
                response = PTP_client(1, grap_up_x, grap_up_y, grap_up_z, grap_up_r)  # houmian,shangfang
                new_x = int(grap_up_x + 1.25 * (160 - x))
                new_y = int(grap_up_y + 1.25 * (120 - y))
                response = PTP_client(1, new_x, new_y, grap_down_z, grap_down_r)  # houmian,fangxia
                response = end_client(1, 1, True)
                rospy.sleep(t1)
                response = PTP_client(1, grap_up_x, grap_up_y, grap_up_z, grap_up_r)  # houmian,shangfang
                response = PTP_client(1, put_up_x, put_up_y, put_up_z, put_up_r)  # qianmian,shangfang
                response = PTP_client(1, put_down_x, put_down_y, put_down_z, put_down_r)  # qianmian,fangxia
                response = end_client(0, 0, True)
                rospy.sleep(t1)
                response = PTP_client(1, put_up_x, put_up_y, put_up_z, put_up_r)  # qianmian,shangfang
                # print("grap_down_x", grap_down_x, "grap_down_y", grap_down_y)
            except rospy.ServiceException, e:
                print
                "Service call failed: %s" % e
            time.sleep(2)
            send_goal(dic[destination])  # 去往目的地

        else:  # 到达省份盒子
            # 机械臂将快件放到盒子里
            # TODO
            rospy.wait_for_service('DobotServer/SetEndEffectorSuctionCup')
            rospy.wait_for_service('DobotServer/SetPTPCmd')
            t2 = rospy.Duration(1, 0)
            try:
                end_client = rospy.ServiceProxy('DobotServer/SetEndEffectorSuctionCup', SetEndEffectorSuctionCup)
                PTP_client = rospy.ServiceProxy('DobotServer/SetPTPCmd', SetPTPCmd)
                response = PTP_client(1, put_down_x, put_down_y, put_down_z, put_down_r)
                response = end_client(1, 1, True)
                rospy.sleep(t2)
                response = PTP_client(1, put_up_x, put_up_y, put_up_z, put_up_r)  # qianmian,shangfang
                response = PTP_client(1, deliver_up_x, deliver_up_y, deliver_up_z, deliver_up_r)
                response = end_client(0, 0, True)
                response = PTP_client(1, grap_up_x, grap_up_y, grap_up_z, grap_up_r)  # houmian,shangfang
            except rospy.ServiceException, e:
                print
                "Service call failed: %s" % e
            time.sleep(2)
            send_goal(str(desk_goal + 1))

    else:
        print("导航失败")


def init_listener():
    global start_ocr_pub
    global goal_pub
    global check_pub
    global pause_nav
    rospy.Subscriber('move_base/result', MoveBaseActionResult, nav_callback)  # 订阅导航结果话题数据
    start_ocr_pub = rospy.Publisher('start_ocr', String, queue_size=1)  # 开始orc指令发布器
    goal_pub = rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)  # 目标点发布器
    check_pub = rospy.Publisher('check', String, queue_size=1)  # 微调发布器
    pause_nav = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)  # 暂停导航发布器


def get_key():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def init_key_listener():
    global settings
    settings = termios.tcgetattr(sys.stdin)
    try:
        while 1:
            key = get_key()
            if key in operation_keys:
                print(key)
                if key == 'k':
                    print('停止导航,关闭程序')
                    # 关闭气泵
                    time.sleep(1)
                    os._exit(1)  # 关闭程序
                if key == '1':
                    recvData = "1111"
                    print(recvData + '恢复导航\n')
                if key == '2':
                    print('暂停导航')
                    pause_nav.publish(GoalID())  # 暂停导航
    except Exception as e:
        print e
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


def load_nodes():
    # for i in (0, 27):
    #     node_list.append(NodeCoordinate())

    f = open("node_coordinate.txt", "r")
    for i in range(12):
        p_x = f.readline()
        p_y = f.readline()
        p_z = f.readline()
        o_x = f.readline()
        o_y = f.readline()
        o_z = f.readline()
        o_w = f.readline()
        node_list.append(NodeCoordinate(p_x, p_y, p_z, o_x, o_y, o_z, o_w))


if __name__ == '__main__':
    rospy.init_node('eaibot_main_node', anonymous=True)
    load_nodes()
    main_thread = threading.Thread(target=main)  # 开一个线程处理任务
    main_thread.start()
    key_thread = threading.Thread(target=init_key_listener)  # 开一个线程处理键盘监听
    key_thread.start()
