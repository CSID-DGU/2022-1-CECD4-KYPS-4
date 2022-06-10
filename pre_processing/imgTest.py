import cv2
import skeletonDetection

protoFile = "2022-1-CECD4-KYPS-4\pre_processing\models\pose_deploy_linevec_faster_4_stages.prototxt"
weightFile = "2022-1-CECD4-KYPS-4\pre_processing\models\pose_iter_160000.caffemodel"
net = skeletonDetection.load_model(protoFile, weightFile)

imgPath = "2022-1-CECD4-KYPS-4\pre_processing\data\data2.jpeg"
img = cv2.imread(imgPath)

resultImg, points = skeletonDetection.detect(net, img)

for point in points:
    print(point)
cv2.imshow("Output-Keypoints",resultImg)
cv2.waitKey(0)
