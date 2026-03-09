#!/usr/bin/env python3
import sys
import rospy
import actionlib
from beginner_tutorials.msg import TimerAction, TimerGoal

def feedback_cb(feedback):
    rospy.loginfo("피드백: %d초 경과 (%.0f%%)",
                 feedback.current_seconds, feedback.progress_percent)

def timer_client(seconds):
    client = actionlib.SimpleActionClient('timer', TimerAction)
    rospy.loginfo("서버 연결 대기...")
    client.wait_for_server()

    goal = TimerGoal()
    goal.target_seconds = seconds

    rospy.loginfo("%d초 타이머 시작!", seconds)
    client.send_goal(goal, feedback_cb=feedback_cb)
    client.wait_for_result()

    result = client.get_result()
    if result.success:
        rospy.loginfo("완료! 총 %d초 소요", result.elapsed_seconds)
    else:
        rospy.logwarn("타이머 실패 또는 취소")

if __name__ == '__main__':
    rospy.init_node('timer_client')
    seconds = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    timer_client(seconds)