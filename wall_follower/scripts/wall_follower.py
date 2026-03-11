#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# ===== 파라미터 =====
DIST_THRESHOLD = 0.8   # 벽까지 이 거리 이내면 "가깝다"고 판단 (m)
LINEAR_SPEED = 0.3   # 전진 속도 (m/s)
ANGULAR_SPEED = 0.5    # 회전 속도 (rad/s)

class WallFollower:
    def __init__(self):
        rospy.init_node('wall_follower')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.regions = {}
        self.state = 'find_wall'
        self.rate = rospy.Rate(10)

    def scan_callback(self, scan):
        # LaserScan 데이터를 5개 영역으로 분할
        self.regions = {
            'right':       min(min(scan.ranges[0:144]),   10),
            'front_right': min(min(scan.ranges[144:288]), 10),
            'front':       min(min(scan.ranges[288:432]), 10),
            'front_left':  min(min(scan.ranges[432:576]), 10),
            'left':        min(min(scan.ranges[576:720]), 10),
        }

    def decide_state(self):
        r = self.regions
        if not r:
            return

        d = DIST_THRESHOLD

        if   r['front'] > d and r['front_left'] > d and r['left'] > d:
            self.state = 'find_wall'
        elif r['front'] < d:
            self.state = 'turn_right'
        else:
            self.state = 'follow_wall'

    def act(self):
        twist = Twist()

        if self.state == 'find_wall':
            # 벽을 찾을 때까지 전진 + 약간 우회전
            twist.linear.x = LINEAR_SPEED
            twist.angular.z = ANGULAR_SPEED
        elif self.state == 'turn_right':
            # 전방에 벽 → 좌회전
            twist.angular.z = -ANGULAR_SPEED
        elif self.state == 'follow_wall':
            # 오른쪽에 벽 → 직진
            twist.linear.x = LINEAR_SPEED

        self.pub.publish(twist)

    def run(self):
        rospy.loginfo("Wall Follower 시작 — 상태: find_wall")
        while not rospy.is_shutdown():
            self.decide_state()
            self.act()
            if self.regions:
                rospy.loginfo("상태: %-12s | 전방: %.2f | 우전방: %.2f | 우측: %.2f",
                              self.state,
                              self.regions['front'],
                              self.regions['front_left'],
                              self.regions['left'])
            self.rate.sleep()

if __name__ == '__main__':
    try:
        wf = WallFollower()
        wf.run()
    except rospy.ROSInterruptException:
        pass