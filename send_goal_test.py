import time

import rospy
from move_base_msgs.msg import MoveBaseActionGoal

if __name__ == '__main__':
    rospy.init_node("test_send_goal_node", anonymous=True)
    pub = rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)
    time.sleep(5)
    goal_msg = MoveBaseActionGoal()
    goal_msg.goal_id.id = 'A' + str(time.time())
    goal_msg.goal.target_pose.pose.position.x = -0.0201952750817
    goal_msg.goal.target_pose.pose.position.y = -2.51371260114
    goal_msg.goal.target_pose.pose.position.z = 0.138
    goal_msg.goal.target_pose.pose.orientation.x = 0.0
    goal_msg.goal.target_pose.pose.orientation.y = 0.0
    goal_msg.goal.target_pose.pose.orientation.z = 0.0391967644333
    goal_msg.goal.target_pose.pose.orientation.w = 0.999231511542
    goal_msg.goal.target_pose.header.frame_id = 'map'
    # goal_msg.header.seq = 35
    # goal_msg.header.stamp.secs = 1652964005
    # goal_msg.header.stamp.nsecs = 491382868
    # goal_msg.goal.target_pose.header.stamp = rospy.Time.now()
    # goal_msg.goal.target_pose.header.stamp.secs = 1652931657
    # goal_msg.goal.target_pose.header.stamp.nsecs = 209585479
    pub.publish(goal_msg)
