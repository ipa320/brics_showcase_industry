#!/usr/bin/env python
import roslib; roslib.load_manifest('brics_showcase_industry_lbr')
import rospy
# protected region customHeaders on begin #
import actionlib
from kinematics_msgs.srv import *
from geometry_msgs.msg import *
from brics_showcase_industry_interfaces.msg import MoveArmCartFeedback, MoveArmCartResult, MoveArmCartGoal, MoveArmCartAction

rospy.init_node('brics_lbr_test')
rospy.sleep(1.0)

ps = PoseStamped()
ps.header.stamp = rospy.Time.now()
ps.pose.position.x = 0.171
ps.pose.position.y = -0.541
ps.pose.position.z = 0.271

ps.pose.orientation.x = 0.374
ps.pose.orientation.y = 0.927
ps.pose.orientation.z = -0.014
ps.pose.orientation.w = 0.004

print "Creating client"
client = actionlib.SimpleActionClient("/MoveArmCartAction", MoveArmCartAction)
rospy.sleep(1.0)
client_goal = MoveArmCartGoal()
client_goal.pose_goal = ps
print "Sensing goal"
client.send_goal(client_goal)
print "Waiting for result"
client.wait_for_result()
