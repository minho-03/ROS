#!/usr/bin/env python3

import rospy
from beginner_tutorials.srv import AddTwoInts, AddTwoIntsResponse

def handle_calc(req):
    op = rospy.get_param('/operator', 'add')
    
    if op == 'add':         #더하기
        result = req.a + req.b
    elif op == 'sub':       #빼기
        result = req.a - req.b
    elif op == 'mul':       #곱하기
        result = req.a * req.b
    elif op == 'div':       #나누기 (몫만 구하기)
        result = req.a // req.b
    else:
        rospy.logwarn("알 수 없는 연산: %s -> 기본값 add 사용",op)
        result = req.a + req.b

    rospy.loginfo("[%s] %d,%d -> %d", op, req.a, req.b, result)
    return AddTwoIntsResponse(result)

def server():
    rospy.init_node('calc_server')
    rospy.Service('calc', AddTwoInts, handle_calc)
    rospy.loginfo("계산기 서버 시작 (operator 파라미터로 연산 변경)")
    rospy.spin()

if __name__ == '__main__':
    server()