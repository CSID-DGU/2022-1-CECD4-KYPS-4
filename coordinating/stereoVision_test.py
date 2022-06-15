import triangulaton as tri
import cv2
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from pre_processing import skeletonDetection as SD

protoFile = "2022-1-CECD4-KYPS-4\\pre_processing\\models\\pose_deploy_linevec_faster_4_stages.prototxt"
weightFile = "2022-1-CECD4-KYPS-4\\pre_processing\\models\\pose_iter_160000.caffemodel"
net = SD.load_model(protoFile, weightFile)

# Stereo vision setup parameters
B = 20               #Distance between the cameras [cm]
f = 8              #Camera lense's focal length [mm]
alpha = 77        #Camera field of view in the horisontal plane [degrees]

right_imgPath = '2022-1-CECD4-KYPS-4\\coordinating\\data\\data6_right.jpg'
left_imgPath = '2022-1-CECD4-KYPS-4\\coordinating\\data\\data6_left.jpg'

frame_right = cv2.imread(right_imgPath)
frame_left = cv2.imread(left_imgPath)

frame_right = SD.resize_image(frame_right, 400, 300)
frame_left = SD.resize_image(frame_left, 400, 300)

right_img, right_points = SD.detect(net, frame_right)
left_img, left_points = SD.detect(net, frame_left)

cv2.imshow("right", right_img)
cv2.imshow("left", left_img)

center_point_right = right_points[0]
center_point_left = left_points[0]

X, Y, Z = tri.find_location(center_point_right, center_point_left, frame_right, frame_left, B, f, alpha)

print("왼쪽 카메라 부터의 거리")
print("X : " + str(X) + "cm")
print("Y : " + str(-1*Y) + "cm")
print("Z : " + str(Z) + "cm")

cv2.waitKey(0)

