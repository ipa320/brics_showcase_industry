#!/usr/bin/env python
import roslib; roslib.load_manifest('brics_showcase_industry_coordinators')
import rospy

# protected region customHeaders on begin #
import smach
import smach_ros
import time
from brics_showcase_industry_interfaces.msg import PickUpAction, MoveArmCartAction, MoveArmCartGoal
from brics_showcase_industry_interfaces.srv import GetObjectPose
from actionlib import *
from actionlib.msg import *
from smach_ros import ActionServerWrapper
from geometry_msgs.msg import PoseStamped

# protected region customHeaders end #

class coordinator_pickup_impl:
	
	def	__init__(self):
		# protected region initCode on begin #
		self.ps = PoseStamped()
		self.ps2 = PoseStamped()
		self.pshome = PoseStamped()
		self.ps.header.stamp = rospy.Time.now()
		self.ps.pose.position.x = 0.0
		self.ps.pose.position.y = -0.7
		self.ps.pose.position.z = 0.443

		self.ps2.header.stamp = rospy.Time.now()
		self.ps2.pose.position.x = 0.0
		self.ps2.pose.position.y = -0.7
		self.ps2.pose.position.z = 0.403

		self.pshome.header.stamp = rospy.Time.now()
		self.pshome.pose.position.x = 0.366
		self.pshome.pose.position.y = 0.157
		self.pshome.pose.position.z = 0.443

		# protected region initCode end #
		pass

	def getposecb(self, a, b):
		print "Setting Pose based on world model"

		if((rospy.Time.now().to_sec() - b.pose.header.stamp.to_sec()) > 3.0):
			print "Time stamp of detection to old"
			return "aborted"

		self.ps.header.stamp = rospy.Time.now()
		self.ps.pose.position.x = b.pose.pose.position.x
		self.ps.pose.position.y = b.pose.pose.position.y
		self.ps.pose.position.z = 0.343

		self.ps2.header.stamp = rospy.Time.now()
		self.ps2.pose.position.x = b.pose.pose.position.x
		self.ps2.pose.position.y = b.pose.pose.position.y
		self.ps2.pose.position.z = 0.153


	def	configure(self):
		# protected region configureCode on begin #
		# Create a SMACH state machine
		
		sm0 = smach.StateMachine(outcomes=['succeeded','aborted','preempted'], input_keys = ['action_feedback'], output_keys = ['action_feedback'])
		sis = smach_ros.IntrospectionServer('coordinator_pickup', sm0, '/pickup_sm')
		sis.start()
		with sm0:
			smach.StateMachine.add('GET_POSE_FROM_WORLDMODEL', smach_ros.ServiceState('/getObjectPose', GetObjectPose, response_cb=self.getposecb), transitions={'succeeded':'MOVE_OVER_BOX', 'aborted':'aborted'})
			smach.StateMachine.add('MOVE_OVER_BOX', smach_ros.SimpleActionState('MoveArmCart', MoveArmCartAction, goal = MoveArmCartGoal(pose_goal=self.ps)), {'succeeded':'MOVE_DOWN'})
			smach.StateMachine.add('MOVE_DOWN', smach_ros.SimpleActionState('MoveArmCart', MoveArmCartAction, goal = MoveArmCartGoal(pose_goal=self.ps2)), {'succeeded':'MOVE_UP'})
			smach.StateMachine.add('MOVE_UP', smach_ros.SimpleActionState('MoveArmCart', MoveArmCartAction, goal = MoveArmCartGoal(pose_goal=self.ps)), {'succeeded':'MOVE_HOME'})
			smach.StateMachine.add('MOVE_HOME', smach_ros.SimpleActionState('MoveArmCart', MoveArmCartAction, goal = MoveArmCartGoal(pose_goal=self.pshome)), {'succeeded':'succeeded'})
		# Execute SMACH plan
		ActionServerWrapper(
        	'pick_up',
        	PickUpAction,
        	wrapped_container = sm0,
        	succeeded_outcomes = ['succeeded'],
        	aborted_outcomes = ['aborted'],
        	preempted_outcomes = ['preempted'],
			).run_server()

		

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
	try:
		rospy.init_node('coordinator_pickup')
		rospy.sleep(2)
		n = coordinator_pickup()
		n.impl.configure()
		while not rospy.is_shutdown():
				n.run()
			
	except rospy.ROSInterruptException:
		print "Exit"



