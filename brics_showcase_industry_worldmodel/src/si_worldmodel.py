#!/usr/bin/env python
import roslib; roslib.load_manifest('brics_showcase_industry_worldmodel')
import rospy

# protected region customHeaders on begin #
# protected region customHeaders end #

from brics_showcase_industry_interfaces.srv import SetObjectPose 
from brics_showcase_industry_interfaces.srv import GetObjectPose 


class si_worldmodel_impl:
	
	def	__init__(self):
		pass
	
	def	configure(self):
		# protected region configureCode on begin #
		# protected region configureCode end #
		pass
	
	def	update(self):
		# protected region updateCode on begin #
		# protected region updateCode end #
		pass
		
	def	callback_setObjectPose(self, req):
		# protected region user implementation of service callback for setObjectPose on begin #
		# protected region user implementation of service callback for setObjectPose end #
		pass
	def	callback_getObjectPose(self, req):
		# protected region user implementation of service callback for getObjectPose on begin #
		# protected region user implementation of service callback for getObjectPose end #
		pass
	

class si_worldmodel:
	def __init__(self):
		self.impl = si_worldmodel_impl()
		setObjectPose_ = rospy.Service('setObjectPose', SetObjectPose, self.impl.callback_setObjectPose)
		getObjectPose_ = rospy.Service('getObjectPose', GetObjectPose, self.impl.callback_getObjectPose)

	
		
	def run(self):
		self.impl.update()

if __name__ == "__main__":
	try:
		rospy.init_node('si_worldmodel')
		n = si_worldmodel()
		n.impl.configure()
		while not rospy.is_shutdown():
			n.run()
			
	except rospy.ROSInterruptException:
		print "Exit"



