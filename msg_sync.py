#!/usr/bin/env python
import message_filters
import rospy
from nav_msgs.msg import Odometry, Path
from sensor_msgs.msg import Image
from geometry_msgs.msg import TwistStamped

def callback(bgr_image, odom, local_plan, cmd_vel):
	# Solve all of perception here...
	bgr_image_pub.publish(bgr_image)
	odom_pub.publish(odom)
	local_goal_pub.publish(local_plan)
	cmd_vel_pub.publish(cmd_vel)

bgr_image_sub = message_filters.Subscriber('/camera/rgb/image_raw', Image)
odom_sub = message_filters.Subscriber('/RosAria/pose', Odometry)
local_goal_sub = message_filters.Subscriber('/move_base/EBandPlannerROS/global_plan', Path)
cmd_vel_sub = message_filters.Subscriber('/RosAria/cmd_vel_stamped', TwistStamped)

bgr_image_pub = rospy.Publisher('bgr_image_sync', Image, queue_size=1)
odom_pub = rospy.Publisher('odom_sync', Odometry, queue_size=1)
local_goal_pub = rospy.Publisher('local_goal_sync', Path, queue_size=1)
cmd_vel_pub = rospy.Publisher('cmd_vel_sync', TwistStamped, queue_size=1) 
rospy.init_node('msg_sync', anonymous=True)

ts = message_filters.ApproximateTimeSynchronizer([bgr_image_sub, odom_sub, local_goal_sub, cmd_vel_sub], 1, 0.1)
ts.registerCallback(callback)
rospy.spin()

