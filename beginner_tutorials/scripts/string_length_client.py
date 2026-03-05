#!/usr/bin/env python3

import sys
import rospy
from beginner_tutorials.srv import StringLength

def string_length_client(text):
    rospy.wait_for_service('string_length')
    try:
        get_length = rospy.ServiceProxy('string_length', StringLength)
        resp = get_length(text)
        return resp.length
    except rospy.ServiceException as e:
        rospy.logerr("서비스 호출 실패: %s", e)

if __name__ == '__main__':
    rospy.init_node('string_length_client')
    
    if len(sys.argv) < 2:
        sys.exit(1)
        
    text = sys.argv[1]
    result = string_length_client(text)
    
    if result is not None:
        rospy.loginfo("'%s'의 길이: %d", text, result)