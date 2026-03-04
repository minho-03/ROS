#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist  # 거북이 속도 메시지 타입 불러오기

def move_turtle():
    # 1. 발행자 설정: /turtle1/cmd_vel 토픽에 Twist 메시지 발행
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('turtle_circle_node')
    rate = rospy.Rate(10)  # 10Hz (초당 10번 발행)

    # 2. Twist 메시지 객체 생성
    vel = Twist()

    while not rospy.is_shutdown():
        # 3. 값 대입: 직진 속도 2.0, 회전 속도 1.0 (동시에 주면 원을 그림)
        vel.linear.x = 2.0
        vel.angular.z = 1.0

        # 4. 발행 및 로그 출력
        rospy.loginfo("거북이 주행 중 - 선속도: %.1f, 각속도: %.1f", vel.linear.x, vel.angular.z)
        pub.publish(vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        move_turtle()
    except rospy.ROSInterruptException:
        pass
