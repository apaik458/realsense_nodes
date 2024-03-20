#!/usr/bin/env python3
from __future__ import print_function

import roslib
roslib.load_manifest('realsense_nodes')

import rospy
import cv2
import mediapipe as mp

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Point

class image_converter:
    def __init__(self):
        self.bridge = CvBridge()
        
        self.image_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.callback)
        self.image_pub = rospy.Publisher("hand_point_topic", Point)

        self.mp_hands = mp.solutions.hands.Hands()

    def callback(self, data):
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

        results = self.mp_hands.process(cv_image)

        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]

            for id,lm in enumerate(myHand.landmark):
                h,w,c = cv_image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)

                if id == 8:
                    cv2.circle(cv_image, (cx,cy), 5, (0,255,0), cv2.FILLED)
                else:
                    cv2.circle(cv_image, (cx,cy), 5, (255,0,255), cv2.FILLED)

            point_data = Point()

            point_data.x = myHand.landmark[8].x
            point_data.y = myHand.landmark[8].y
            point_data.z = myHand.landmark[8].z

            self.image_pub.publish(point_data)

        cv2.imshow("Image window", cv_image)

        if cv2.waitKey(3) == ord('q'):
            rospy.signal_shutdown("Closing windows")

def main():
    ic = image_converter()

    rospy.init_node('image_converter', anonymous=True)

    rospy.spin()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
