#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class ScanToLed:
    def __init__(self):
        rospy.init_node('scan_to_led_node')
        
        self.min_distance = 99.0 # 초기 거리
        self.current_vel = 0.0   # 초기 속도
        
        # 발행자 (퍼블리셔): 아두이노로 색상 전달
        self.led_pub = rospy.Publisher('/led_color', String, queue_size=10)
        
        # 구독자 (서브스크라이버): 라이다 및 속도 데이터 읽기
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        rospy.Subscriber('/cmd_vel', Twist, self.vel_callback)
        
        rospy.loginfo("Scan to LED Node Started!")

    def scan_callback(self, msg):
        # 전방(-30도 ~ +30도)의 장애물 거리 중 최솟값 찾기
        front_ranges = msg.ranges[0:30] + msg.ranges[-30:]
        # 무한대(inf)나 에러 값 제외하고 최솟값 계산
        valid_ranges = [r for r in front_ranges if 0.0 < r < float('inf')]
        
        if valid_ranges:
            self.min_distance = min(valid_ranges)
        else:
            self.min_distance = 99.0
            
        self.decide_color()

    def vel_callback(self, msg):
        # 로봇의 선속도(앞/뒤) 저장
        self.current_vel = msg.linear.x
        self.decide_color()

    def decide_color(self):
        color_msg = String()
        
        # 1. 물체 근접: 거리가 0.3m(30cm) 이하일 때 무조건 빨강
        if self.min_distance <= 0.3:
            color_msg.data = "RED"
        # 2. 전진 중: 속도가 양수일 때 초록
        elif self.current_vel > 0.0:
            color_msg.data = "GREEN"
        # 3. 후진 중: 속도가 음수일 때 파랑
        elif self.current_vel < 0.0:
            color_msg.data = "BLUE"
        # 4. 정지 및 안전: 꺼짐 (또는 다른 색상 가능)
        else:
            color_msg.data = "OFF"
            
        self.led_pub.publish(color_msg)

if __name__ == '__main__':
    try:
        ScanToLed()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass