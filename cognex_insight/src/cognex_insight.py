#!/usr/bin/env python
import roslib; roslib.load_manifest('cognex_insight')
import rospy

# protected region customHeaders on begin #
import telnetlib
from xml.dom.minidom import parse, parseString
from geometry_msgs.msg import Pose
from tf.transformations import *
# protected region customHeaders end #

from geometry_msgs.msg import PoseArray 


class cognex_insight_impl:
	config_camera_ip = "169.254.7.197"
	config_configuration_port = 23
	config_data_port = 50000
	config_Pose1X_Cell = "['C',50]"
	config_Pose1Y_Cell = "['D',50]"
	config_Pose1Theta_Cell = "['E',50]"
	config_Pose2X_Cell = "['C',51]"
	config_Pose2Y_Cell = "['D',51]"
	config_Pose2Theta_Cell = "['E',51]"
	config_Pose3X_Cell = "['C',52]"
	config_Pose3Y_Cell = "['D',52]"
	config_Pose3Theta_Cell = "['E',52]"
	out_detected_pattern = PoseArray()
	
	def	__init__(self):
		pass
	
	def	configure(self):
		# protected region configureCode on begin #
		tn = telnetlib.Telnet(self.config_camera_ip, self.config_configuration_port)
		print "Connected..."
		tn.read_until("User: ")
		print "sending username..."
		tn.write("admin\r\n")
		tn.read_until("Password: ")
		print "sending password..."
		tn.write("\r\n")
		tn.read_until("User Logged In")
		print "configuring...."
		pose_col, pose_row = eval(self.config_Pose1X_Cell)
		tn.write("Put Watch "+pose_col+"0"+str(pose_row)+" 2\r\n")
		pose_col, pose_row = eval(self.config_Pose1Y_Cell)
		tn.write("Put Watch "+pose_col+"0"+str(pose_row)+" 2\r\n")
		pose_col, pose_row = eval(self.config_Pose1Theta_Cell)
		tn.write("Put Watch "+pose_col+"0"+str(pose_row)+" 2\r\n")
		pose_col, pose_row = eval(self.config_Pose2X_Cell)
		tn.write("Put Watch "+pose_col+"0"+str(pose_row)+" 2\r\n")
		pose_col, pose_row = eval(self.config_Pose2Y_Cell)
		tn.write("Put Watch "+pose_col+"0"+str(pose_row)+" 2\r\n")
		pose_col, pose_row = eval(self.config_Pose2Theta_Cell)
		tn.write("Put Watch "+pose_col+"0"+str(pose_row)+" 2\r\n")
		pose_col, pose_row = eval(self.config_Pose3X_Cell)
		tn.write("Put Watch "+pose_col+"0"+str(pose_row)+" 2\r\n")
		pose_col, pose_row = eval(self.config_Pose3Y_Cell)
		tn.write("Put Watch "+pose_col+"0"+str(pose_row)+" 2\r\n")
		pose_col, pose_row = eval(self.config_Pose3Theta_Cell)
		tn.write("Put Watch "+pose_col+"0"+str(pose_row)+" 2\r\n")
		
		self.tnd = telnetlib.Telnet(self.config_camera_ip, self.config_data_port)
		print "Connected..."
		print "Sending login..."
		self.tnd.write("admin\r\n")
		print "Sending password..."
		self.tnd.write("\r\n")
		self.tnd.read_until("</Prompt>")
		print "Enabling data output..."
		self.tnd.write("dat\r\n")
		# protected region configureCode end #
		pass
	
	def	update(self):
		# protected region updateCode on begin #
		mes = self.tnd.read_until("</Cycle>")
		res = { 0:{}, 1:{}, 2:{}, 3:{} }
		dom = parseString(mes)
		pose_col, pose_row = eval(self.config_Pose1X_Cell)
		p1x=pose_col+str(pose_row)
		pose_col, pose_row = eval(self.config_Pose1Y_Cell)
		p1y=pose_col+str(pose_row)
		pose_col, pose_row = eval(self.config_Pose1Theta_Cell)
		p1th=pose_col+str(pose_row)
		pose_col, pose_row = eval(self.config_Pose2X_Cell)
		p2x=pose_col+str(pose_row)
		pose_col, pose_row = eval(self.config_Pose2Y_Cell)
		p2y=pose_col+str(pose_row)
		pose_col, pose_row = eval(self.config_Pose2Theta_Cell)
		p2th=pose_col+str(pose_row)
		pose_col, pose_row = eval(self.config_Pose3X_Cell)
		p3x=pose_col+str(pose_row)
		pose_col, pose_row = eval(self.config_Pose3Y_Cell)
		p3y=pose_col+str(pose_row)
		pose_col, pose_row = eval(self.config_Pose3Theta_Cell)
		p3th=pose_col+str(pose_row)
		
		for c in dom.getElementsByTagName("Cell"):
			try:
				val = float(c.getElementsByTagName("Float")[0].childNodes[0].data)
			except:
				continue
			if c.attributes['Id'].value == p1x:
				res[0]['x']=val
			elif c.attributes['Id'].value == p1y:
				res[0]['y']=val
			elif c.attributes['Id'].value == p1th:
				res[0]['th']=val
			
			elif c.attributes['Id'].value == p2x:
				res[1]['x']=val
			elif c.attributes['Id'].value == p2y:
				res[1]['y']=val
			elif c.attributes['Id'].value == p2th:
				res[1]['th']=val

			elif c.attributes['Id'].value == p3x:
				res[2]['x']=val
			elif c.attributes['Id'].value == p3y:
				res[2]['y']=val
			elif c.attributes['Id'].value == p3th:
				res[2]['th']=val

		
		for k,v in res.iteritems():
			if v.has_key('x'):
				p = Pose()
				p.position.x = v['x']
				p.position.y = v['y']
				p.position.z = 0
				q = quaternion_about_axis( math.radians(v['th']), (0, 0, 1))
				p.orientation.x = q[0]
				p.orientation.y = q[1]
				p.orientation.z = q[2]
				p.orientation.w = q[3]
				self.out_detected_pattern.poses.append(p)
		# protected region updateCode end #
		pass
		
	

class cognex_insight:
	def __init__(self):
		self.impl = cognex_insight_impl()
		self.detected_pattern = rospy.Publisher('detected_pattern', PoseArray)

	
		
	def run(self):
		self.impl.update()
		self.detected_pattern.publish(self.impl.out_detected_pattern)

if __name__ == "__main__":
	try:
		rospy.init_node('cognex_insight')
		n = cognex_insight()
		n.impl.configure()
		while not rospy.is_shutdown():
			n.run()
			rospy.sleep(1/100.0)
			
	except rospy.ROSInterruptException:
		print "Exit"



