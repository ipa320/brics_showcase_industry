#!/usr/bin/env python
import roslib; roslib.load_manifest('brics_showcase_industry_coordinators')
import rospy

# protected region customHeaders on begin #
import smach
import smach_ros
import time
from brics_showcase_industry_interfaces.msg import MoveArmCartAction, MoveArmCartGoal
from actionlib import *
from actionlib.msg import *
from geometry_msgs.msg import PoseStamped

# protected region customHeaders end #

class coordinator_pickup_impl:
	
	def	__init__(self):
		# protected region initCode on begin #

		# protected region initCode end #
		pass
	
	def	configure(self):
		# protected region configureCode on begin #
		# Create a SMACH state machine
		ps = PoseStamped()
		ps.pose.position.x = 100
		ps.pose.position.y = 100
		ps.pose.position.z = 100

    	sm0 = smach.StateMachine(outcomes=['succeeded','aborted','preempted'])
    	with sm0:
    		smach.StateMachine.add('MOVE_OVER_BOX', smach_ros.SimpleActionState('MoveArmCart', MoveArmCartAction, goal = MoveArmCartGoal(pose_goal=1)), {'succeeded':'succeeded'})
		# protected region configureCode end #
		pass
	
	def	update(self):
		# protected region updateCode on begin #
		# protected region updateCode end #
		pass
		
	

class coordinator_pickup:
	def __init__(self):
		self.impl = coordinator_pickup_impl()

	
		
	def run(self):
		self.impl.update()

if __name__ == "__main__":
	print "hallopallo\n\n\n\n\n"
	try:
		print "hallopallo"
		rospy.init_node('coordinator_pickup')
		rospy.sleep(2)
		#n = coordinator_pickup()
		#n.impl.configure()
		#while not rospy.is_shutdown():
		#		n.run()
			
	except rospy.ROSInterruptException:
		print "Exit"



