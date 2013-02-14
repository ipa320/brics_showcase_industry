#!/usr/bin/env python
import roslib; roslib.load_manifest('brics_showcase_industry_transformer')
import rospy

# protected region customHeaders on begin #
from geometry_msgs.msg import PoseStamped, Pose
from brics_showcase_industry_interfaces.srv import SetObjectPose, SetObjectPoseRequest
import copy
# protected region customHeaders end #

from geometry_msgs.msg import PoseArray 


class pose_transformer_impl:
	config_CameraPose = "[[0,0,0],[0,0,0,0]]"
	config_MeterPerPixel = 0.000589
	in_CameraDetections = PoseArray()
	
	def	__init__(self):
		# protected region initCode on begin #
		self.worldmodel_client = rospy.ServiceProxy('setObjectPose', SetObjectPose)
		self.config_ResolutionX = 1600.0
		self.config_ResolutionY = 1200.0
		# protected region initCode end #
		pass
	
	def	configure(self):
		# protected region configureCode on begin #
		# protected region configureCode end #
		pass
	
	def	update(self):
		# protected region updateCode on begin #
		in_CameraDetections = copy.deepcopy(self.in_CameraDetections)
		
		if len(in_CameraDetections.poses) <= 0:
			return
			
		out_CameraDetections = PoseArray()
		for pose in in_CameraDetections.poses:
			print pose.position.x , pose.position.y
			print pose.position.x - self.config_ResolutionX/2.0, pose.position.y - self.config_ResolutionY/2.0
			new_pose = Pose()
			new_pose.position.x = (pose.position.x - self.config_ResolutionX/2.0) * self.config_MeterPerPixel
			new_pose.position.y = (pose.position.y - self.config_ResolutionY/2.0) * self.config_MeterPerPixel
			new_pose.position.z = 0.0
			new_pose.orientation = pose.orientation
			out_CameraDetections.poses.append(new_pose)
		
		print out_CameraDetections
		

		try:
			rospy.wait_for_service('setObjectPose', 5)
		except rospy.ROSException, e:
			print "%s"%e
			return

		try:
			req = SetObjectPoseRequest()
			req.pose.header.stamp = rospy.Time.now() ## HACK: filling timestamp here because no one is assigned by detection node
			req.pose.header.frame_id = "/camera_base_link"
			req.pose.pose = out_CameraDetections.poses[0] ## HACK: only using first pose
			res = self.worldmodel_client(req)
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
		# protected region updateCode end #
		pass
		
	

class pose_transformer:
	def __init__(self):
		self.impl = pose_transformer_impl()
		self.CameraDetections = rospy.Subscriber("/detected_pattern",PoseArray, self.CameraDetectionsCallback) 

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



