#!/usr/bin/env python
import roslib; roslib.load_manifest('brics_showcase_industry_coordinators')
import rospy

# protected region customHeaders on begin #
import smach
import smach_ros
import time
from brics_showcase_industry_interfaces.msg import PickUpAction, DropDownAction
from actionlib import *
from actionlib.msg import *
# protected region customHeaders end #



class coordinator_application_impl:
	
	def	__init__(self):
		# protected region initCode on begin #

		sm0 = smach.StateMachine(outcomes=['succeeded','aborted','preempted'])
		sis = smach_ros.IntrospectionServer('coordinator_application', sm0, '/SM_ROOT')
		sis.start()
		sis.start()
		with sm0:
			smach.StateMachine.add('PICKUP_OBJECT', smach_ros.SimpleActionState('pick_up', PickUpAction), {'succeeded':'succeeded'})
			#smach.StateMachine.add('DROP_OBJECT', smach_ros.SimpleActionState('drop_down', DropDownAction), {'succeeded':'succeeded'})
		# Execute SMACH plan
		outcome = sm0.execute()
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
		
	

class coordinator_application:
	def __init__(self):
		self.impl = coordinator_application_impl()

	
		
	def run(self):
		self.impl.update()

if __name__ == "__main__":
	try:
		rospy.init_node('coordinator_application')
		n = coordinator_application()
		n.impl.configure()
		while not rospy.is_shutdown():
			n.run()
			
	except rospy.ROSInterruptException:
		print "Exit"



