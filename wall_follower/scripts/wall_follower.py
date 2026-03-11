#!/usr/bin/env python3
import rospy
import math
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# ===== 주행 파라미터 최적화 =====
LINEAR_SPEED = 0.4       # 속도를 약간 높임
MAX_ANGULAR_SPEED = 1.0  # 회전 속도 제한
DESIRED_DISTANCE = 1.0   # 벽과의 거리

class WallFollowerPID:
    def __init__(self):
        rospy.init_node('wall_follower_pid')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        self.kp = 1.8
        self.ki = 0.5
        self.kd = 0.03

        self.integral = 0.0
        self.prev_error = 0.0
        self.dt = 0.1 
        self.rate = rospy.Rate(10)

    def get_range(self, scan, angle):
        index = int((angle - scan.angle_min) / scan.angle_increment)
        index = max(0, min(index, len(scan.ranges) - 1))
        distance = scan.ranges[index]
        # 문(Gap) 구간에서 데이터가 튀는 것을 방지하기 위해 최대치 제한
        if math.isnan(distance) or math.isinf(distance) or distance > 5.0:
            distance = 5.0
        return distance

    def get_error(self, scan, desired_distance):
        # 1. 각도를 다시 안정적인 정측면(90도) 근처로 복구
        theta = math.radians(30)
        a = self.get_range(scan, math.radians(60))  # 왼쪽 대각선 앞
        b = self.get_range(scan, math.radians(90))  # 왼쪽 직각

        # 2. 기하학적 거리 계산
        alpha = math.atan2(a * math.cos(theta) - b, a * math.sin(theta))
        current_dist = b * math.cos(alpha)
        
        # 3. 오차 계산 (이 값이 양수면 벽과 멀어져야 함)
        return desired_distance - current_dist

    def pid_control(self, error):
        p_term = self.kp * error
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        d_term = self.kd * (error - self.prev_error) / self.dt
        self.prev_error = error

        # [중요] 부호 체크! 
        # 왼쪽 벽 주행 시: 
        # 오차가 (+)다 = 벽과 너무 가깝다 -> 오른쪽으로 꺾어야 함 (음수 값)
        # 오차가 (-)다 = 벽과 너무 멀다 -> 왼쪽으로 꺾어야 함 (양수 값)
        # 따라서 계산된 값에 마이너스(-)를 붙여줍니다.
        angular_z = -(p_term + i_term + d_term) 

        # 너무 급하게 돌지 않도록 제한
        angular_z = np.clip(angular_z, -0.8, 0.8)

        twist = Twist()
        twist.linear.x = LINEAR_SPEED
        twist.angular.z = angular_z
        self.pub.publish(twist)

    def scan_callback(self, scan):
        # 전방 감지 범위를 넓혀서 코너를 미리 감지
        front = self.get_range(scan, 0.0)
        error = self.get_error(scan, DESIRED_DISTANCE)

        # 전방에 벽이 있으면(ㄱ자 꺾임) 더 과감하게 회전
        if front < 0.8:
            twist = Twist()
            twist.linear.x = 0.05  # 속도 대폭 감속
            twist.angular.z = -0.8  # 우회전 (왼쪽 벽을 따라가므로 우회전해야 함)
            self.pub.publish(twist)
            rospy.loginfo("코너/문 감지 - 감속 선회 중...")
        else:
            self.pid_control(error)

if __name__ == '__main__':
    try:
        wf = WallFollowerPID()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass