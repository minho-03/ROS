#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose

def pose_callback(data):
    rospy.loginfo("거북이 위치 추적 중 -> x: %.2f, y: %.2f", data.x, data.y)

def listener():
    rospy.init_node('pose_listener')
    rospy.Subscriber("/turtle1/pose", Pose, pose_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()