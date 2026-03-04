#!/usr/bin/env python3
import rospy
import random
from std_msgs.msg import Float32

def temp_publisher():
    # 'temperature' 토픽으로 Float32형 메시지 발행 설정
    pub = rospy.Publisher('temperature', Float32, queue_size=10)
    rospy.init_node('temp_pub_node')
    rate = rospy.Rate(1) # 1초에 1번 실행
    
    while not rospy.is_shutdown():
        # 20.0 ~ 40.0 사이의 랜덤 소수점 숫자 생성
        current_temp = random.uniform(20.0, 40.0)
        rospy.loginfo("현재 온도 발행: %.2f", current_temp)
        pub.publish(current_temp)
        rate.sleep()

if __name__ == '__main__':
    try:
        temp_publisher()
    except rospy.ROSInterruptException:
        pass
