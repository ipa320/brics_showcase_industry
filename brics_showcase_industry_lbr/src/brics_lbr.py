#!/usr/bin/env python
import roslib; roslib.load_manifest('brics_showcase_industry_lbr')
import rospy

# protected region customHeaders on begin #
import actionlib
from kinematics_msgs.srv import *
from brics_showcase_industry_interfaces.msg import MoveArmCartFeedback, MoveArmCartResult, MoveArmCartGoal, MoveArmCartAction
# protected region customHeaders end #



class brics_lbr_impl:
	
	def	__init__(self):
		# protected region initCode on begin #
		self.iks = rospy.ServiceProxy('/arm_kinematics/get_ik', GetPositionIK)
		# protected region initCode end #
		pass
	
	def	configure(self):
		# protected region configureCode on begin #
		# protected region configureCode end #
		pass
	
	def	update(self):
		# protected region updateCode on begin #
		print "blub"
		# protected region updateCode end #
		pass

	def callIKSolver(self, current_pose, goal_pose):
		req = GetPositionIKRequest()
		req.ik_request.ik_link_name = "arm_7_link"		#ToDo: consider ${prefix} from ur5_description
		req.ik_request.ik_seed_state.joint_state.position = current_pose
		req.ik_request.pose_stamped = goal_pose
		resp = self.iks(req)
		result = []
		for o in resp.solution.joint_state.position:
			result.append(o)
		return (result, resp.error_code)

	def execute_MoveArmCart_callback(self, goal):
		_MoveArmCart_feedback = MoveArmCartFeedback()
		_MoveArmCart_result = MoveArmCartResult()
		# protected region updateCode on begin #

		(grasp_conf, error_code) = self.callIKSolver([0,0,0,0,0,0,0], goal.pose_goal)		
		if(error_code.val != error_code.SUCCESS):
			self.retries += 1
			rospy.logerr("Ik grasp Failed")
			sss.set_light('led_off')
			return 'failed'

		# protected region updateCode end #
		pass
		
	

class brics_lbr:
	def __init__(self):
		self.impl = brics_lbr_impl()
		self.impl._as = actionlib.SimpleActionServer("MoveArmCartAction", MoveArmCartAction, execute_cb=self.impl.execute_MoveArmCart_callback)
		self.impl._as.start()

	
		
	def run(self):
		self.impl.update()

if __name__ == "__main__":
	try:
		rospy.init_node('brics_lbr')
		n = brics_lbr()
		n.impl.configure()
		while not rospy.is_shutdown():
			n.run()
			
	except rospy.ROSInterruptException:
		print "Exit"



