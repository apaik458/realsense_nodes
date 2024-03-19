#!/usr/bin/env python3
from __future__ import print_function

import roslib
roslib.load_manifest('realsense_nodes')

import rospy
import cv2
import mediapipe as mp

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class image_converter:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.callback)

        self.mp_hands = mp.solutions.hands.Hands()

    def callback(self, data):
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

        ### Hand detection ###############################################
        results = self.mp_hands.process(cv_image)

        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]

            for id,lm in enumerate(myHand.landmark):
                h,w,c = cv_image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                cv2.circle(cv_image, (cx,cy), 5, (255,0,255), cv2.FILLED)

        cv2.imshow("Image window", cv_image)
        ##################################################################

        if cv2.waitKey(3) == ord('q'):
            rospy.signal_shutdown("Closing windows")

def main():
    ic = image_converter()

    rospy.init_node('image_converter', anonymous=True)

    rospy.spin()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
