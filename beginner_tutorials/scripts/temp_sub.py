#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32

def callback(msg):
    # 온도가 35.0도 이상일 때만 경고 메시지 출력
    if msg.data >= 35.0:
        rospy.logwarn("⚠️ 경고! 고온 감지: %.2f", msg.data)
    else:
        rospy.loginfo("온도 정상: %.2f", msg.data)

def temp_subscriber():
    rospy.init_node('temp_sub_node')
    rospy.Subscriber('temperature', Float32, callback)
    rospy.spin()

if __name__ == '__main__':
    temp_subscriber()
