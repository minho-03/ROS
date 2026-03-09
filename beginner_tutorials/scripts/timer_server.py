#!/usr/bin/env python3
import rospy
import actionlib
from beginner_tutorials.msg import TimerAction, TimerFeedback, TimerResult

class TimerServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer(
            'timer',
            TimerAction,
            execute_cb=self.execute,
            auto_start=False
        )
        self.server.start()
        rospy.loginfo("타이머 서버 시작")

    def execute(self, goal):
        rospy.loginfo("목표 수신: %d초 타이머", goal.target_seconds)

        feedback = TimerFeedback()
        rate = rospy.Rate(1)

        for i in range(1, goal.target_seconds + 1):
            # 취소 요청 확인
            if self.server.is_preempt_requested():
                rospy.logwarn("타이머 취소됨!")
                self.server.set_preempted()
                return

            # 피드백 전송
            feedback.current_seconds = i
            feedback.progress_percent = (i / goal.target_seconds) * 100
            self.server.publish_feedback(feedback)
            rospy.loginfo("  진행: %d/%d초 (%.0f%%)",
                         i, goal.target_seconds, feedback.progress_percent)
            rate.sleep()

        # 완료 결과 전송
        result = TimerResult()
        result.success = True
        result.elapsed_seconds = goal.target_seconds
        self.server.set_succeeded(result)
        rospy.loginfo("타이머 완료!")

if __name__ == '__main__':
    rospy.init_node('timer_server')
    TimerServer()
    rospy.spin()