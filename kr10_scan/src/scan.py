#!/usr/bin/env python3

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import *
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import rospkg
import os


class Scanner:
    def __init__(self):
        rospy.init_node("scanner", anonymous=True)

        moveit_commander.roscpp_initialize(sys.argv)

        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()


        group_name = "arm"
        self.move_group = moveit_commander.MoveGroupCommander(group_name)
        print("defined move_group")

        self.display_trajectory_publisher = rospy.Publisher(
            "/move_group/display_planned_path",
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=20,
        )
        self.sub = rospy.Subscriber('/rrbot/camera1/image_raw', Image, self.camera_cb)
        self.image_path = self.file_path = rospkg.RosPack().get_path('kr10_scan')+'/images'
        self.bridge = CvBridge
        self.image_data = None

    def GoToGoal(self, x, y, z):
        print(f"Going to {x} {y} {z}")
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.w = 1.0
        pose_goal.position.x = x
        pose_goal.position.y = y
        pose_goal.position.z = z
        self.move_group.set_pose_target(pose_goal)

        plan = self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()
    
    def TakePic(self, i):
        print("Take Pic")
        bridge = CvBridge()
        try:
            img = bridge.imgmsg_to_cv2(self.image_data, "bgr8")
        except CvBridgeError as e:
            print(e)
        print("Took Pic "+str(i)+" !!")
        filename = 'Image_'+str(i)+'.jpg'
        cv2.imwrite(os.path.join(self.image_path, filename), img)

    def run(self):
        poses = [[0.152, 0.468, 0.617], [0, 0, 0.74], [0, -0.932, 0], [0, 0, -0.74]]
        #Get strating position coordinates
        print("Going to intial pose")
        wpose = geometry_msgs.msg.Pose()
        wpose.orientation.w = 1.0
        wpose.position.x = poses[0][0]
        wpose.position.y = poses[0][1]
        wpose.position.z = poses[0][2]
        self.GoToGoal(poses[0][0], poses[0][1], poses[0][2])
        self.TakePic(0)
        
        print("Starting path")
        for i, pose in enumerate(poses[1:]):
            wpose.position.x += pose[0]  
            wpose.position.y += pose[1]  
            wpose.position.z += pose[2]
            self.GoToGoal(wpose.position.x, wpose.position.y, wpose.position.z)
            self.TakePic(i+1)

    def camera_cb(self, data):
        # rospy.loginfo("callback")
        # print(len(data.data))
        # print("encoding ", data.encoding)
        self.image_data = data



if __name__ == '__main__':
    scanner = Scanner()
    scanner.run()

    # rospy.spin()