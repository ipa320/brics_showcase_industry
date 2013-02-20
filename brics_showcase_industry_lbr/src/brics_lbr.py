#!/usr/bin/env python
import roslib; roslib.load_manifest('brics_showcase_industry_lbr')
import rospy

# protected region customHeaders on begin #
from kinematics_msgs.srv import *
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
		
	

class brics_lbr:
	def __init__(self):
		self.impl = brics_lbr_impl()

	
		
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



