#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose # 거북이 위치(Pose) 메시지 타입

def callback(data):
    # 거북이 화면은 0.0 ~ 11.0 사이의 좌표를 가짐
    # 벽에 가까워지는 조건: 1.0 이하이거나 10.0 이상일 때
    if data.x < 1.0 or data.x > 10.0 or data.y < 1.0 or data.y > 10.0:
        rospy.logerr("🚨 [위험] 벽 충돌 주의! 현재 위치 - x: %.1f, y: %.1f", data.x, data.y)
    else:
        rospy.loginfo("안전 주행 중 - x: %.1f, y: %.1f", data.x, data.y)

def listener():
    rospy.init_node('turtle_pos_monitor')
    # /turtle1/pose 토픽을 구독하여 위치 정보(Pose)를 받아옴
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
