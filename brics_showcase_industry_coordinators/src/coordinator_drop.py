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



class coordinator_drop_impl:
	
	def	__init__(self):
		# protected region initCode on begin #
		# protected region initCode end #
		pass
	
	def	configure(self):
		# protected region configureCode on begin #
		# protected region configureCode end #
		pass
	
	def	update(self):
		# protected region updateCode on begin #
		# protected region updateCode end #
		pass
		
	

class coordinator_drop:
	def __init__(self):
		self.impl = coordinator_drop_impl()

	
		
	def run(self):
		self.impl.update()

if __name__ == "__main__":
	try:
		rospy.init_node('coordinator_drop')
		n = coordinator_drop()
		n.impl.configure()
		while not rospy.is_shutdown():
			n.run()
			
	except rospy.ROSInterruptException:
		print "Exit"



