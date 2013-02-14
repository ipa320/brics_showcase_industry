#!/usr/bin/env python
import roslib; roslib.load_manifest('brics_showcase_industry_transformer')
import rospy

# protected region customHeaders on begin #
# protected region customHeaders end #

from geometry_msgs.msg import PoseArray 

import actionlib
from brics_showcase_industry_interfaces.msg import FindObjectsFeedback, FindObjectsResult, FindObjectsGoal, FindObjectsAction


class pose_transformer_impl:
	config_CameraPose = "[[0,0,0],[0,0,0,0]]"
	in_CameraDetections = PoseArray()
	
	def	__init__(self):
		pass
	
	def	configure(self):
		# protected region configureCode on begin #
		# protected region configureCode end #
		pass
	
	def	update(self):
		# protected region updateCode on begin #
		if(FindObjectAction_handler.status == "Running"):
			dosomething
			if(everything_done == True):
				FindObjectAction_handler.status = "Finished"
		# protected region updateCode end #
		pass

	def execute_FindObject_callback(self, goal):
		_find_objects_feedback = FindObjectsFeedback()
		_find_objects_result = FindObjectsResult()
		# protected region updateCode on begin #

		# protected region updateCode end #
		pass
		
	

class pose_transformer:
	def __init__(self):
		self.impl = pose_transformer_impl()
		self.CameraDetections = rospy.Subscriber("CameraDetections",PoseArray, self.CameraDetectionsCallback) 
		self._as = actionlib.SimpleActionServer("FindObjectsAction", FindObjectsAction, execute_cb=self.impl.execute_FindObject_callback)
    	self._as.start()

	def CameraDetectionsCallback(self, a):
		self.impl.in_CameraDetections = a
	
		
	def run(self):
		self.impl.update()

if __name__ == "__main__":
	try:
		rospy.init_node('pose_transformer')
		n = pose_transformer()
		n.impl.configure()
		while not rospy.is_shutdown():
			n.run()
			
	except rospy.ROSInterruptException:
		print "Exit"



