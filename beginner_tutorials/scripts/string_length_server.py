#!/usr/bin/env python3
import rospy
from beginner_tutorials.srv import StringLength, StringLengthResponse

def handle_length(req):
    result = len(req.text)
    rospy.loginfo("요청: '%s' → 길이: %d", req.text, result)
    return StringLengthResponse(result)

def server():
    rospy.init_node('string_length_server')
    rospy.Service('string_length', StringLength, handle_length)
    rospy.loginfo("문자열 길이 서버 준비 완료")
    rospy.spin()
    
if __name__ == '__main__':

    server()
