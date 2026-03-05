#!/usr/bin/env python3

import rospy

from turtlesim.srv import SetPen

def change_pen(r,g,b,width):
    rospy.wait_for_service('/turtle1/set_pen')
    try:
        set_pen = rospy.ServiceProxy('/turtle1/set_pen',SetPen)
        set_pen(r,g,b,width,0)
        rospy.loginfo("펜 변경: R=%d G=%d B=%d 두께=%d", r,g,b,width)
    except rospy.ServiceException as e:
        rospy.logerr("실패: %s", e)

if __name__=='__main__':
    rospy.init_node('change_pen_client')
    change_pen(255,255,0,10) #노란색, 두께 10