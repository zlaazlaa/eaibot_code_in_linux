# coding=utf-8
import os
import select
import sys
import termios
import time
import tty
import rospy
from actionlib_msgs.msg import GoalID
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionResult
from std_msgs.msg import String

operation_keys = ['1','2', '3', '4', 'k']
now_goal = '0'  # 记录当前导航目标点
node_list = []
dic = {'四川': 0, '安徽': 1, '湖南': 2, '广东': 3, '浙江': 4, '江苏': 5, '福建': 6, '河南': 7, 'none': 0}

start_ocr_pub = rospy.Publisher('/start_ocr', String, queue_size=1)  # 开始orc指令发布器
goal_pub = rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)  # 目标点发布器
check_pub = rospy.Publisher('check', String, queue_size=1)  # 微调发布器
pause_nav = rospy.Publisher('move_base/cancel', GoalID, queue_size=1)  # 暂停导航发布器


class NodeCoordinate:
    def __init__(self):
        p = []
        self.p_x = 0.0
        self.p_y = 0.0
        self.p_z = 0.0
        self.o_x = 0.0
        self.o_y = 0.0
        self.o_z = 0.0
        self.o_w = 0.0


def send_goal(i):  # Go to point i
    global now_goal
    now_goal = i
    goal_msg = MoveBaseActionGoal()
    goal_msg.goal_id.id = i + '_' + time.time()
    goal_msg.goal.target_pose.pose.position.x = node_list[i].p[0]
    goal_msg.goal.target_pose.pose.position.y = node_list[i].p[1]
    goal_msg.goal.target_pose.pose.position.z = node_list[i].p[2]
    goal_msg.goal.target_pose.pose.orientation.x = node_list[i].p[3]
    goal_msg.goal.target_pose.pose.orientation.y = node_list[i].p[4]
    goal_msg.goal.target_pose.pose.orientation.z = node_list[i].p[5]
    goal_msg.goal.target_pose.pose.orientation.w = node_list[i].p[6]
    goal_pub.publish(goal_msg)


def main():
    for i in ('8', '27'):
        send_goal(i)


def nav_callback(data):
    if data.status.status == 3:
        goal_name = data.status.goal_id.id.split('_')[0]
        if goal_name >= '8':  # 到达分拣台
            # 机械臂伸展开
            # TODO
            time.sleep(2)
            start_ocr_pub.publish("start_ocr")
            ocr_result = rospy.wait_for_message('/ocr_result', String, timeout=None)
            result = str(ocr_result).split('_')
            destination = result[0]
            x = int(result[1])
            y = int(result[2])
            # 机械臂抓取
            # TODO
            time.sleep(2)
            # 机械臂将邮件放到车上
            # TODO
            time.sleep(2)
            send_goal(destination)  # 去往目的地

        else:  # 到达省份盒子
            # 机械臂将快件放到盒子里
            # TODO
            time.sleep(2)
            # 机械臂归位
            # TODO
            time.sleep(2)

    else:
        print("导航失败")


def init_listener():
    rospy.Subscriber('move_base/result', MoveBaseActionResult, nav_callback)  # 订阅导航结果话题数据


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
                    send_goal(now_goal)
                if key == '2':
                    print('已经暂停导航')
                    pause_nav.publish(GoalID())  # 暂停导航
    except Exception as e:
        print e
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


def load_nodes():
    # for i in (0,27):
    # node_list.append(NodeCoordinate())

    f = open("node_coordinate.txt", "r")
    for i in (0, 27):
        for j in (0, 6):
            node_list[i].p.append(f.readline())


if __name__ == '__main__':
    rospy.init_node('eaibot_main_node', anonymous=True)
    init_listener()
    init_key_listener()
    load_nodes()
    main()
