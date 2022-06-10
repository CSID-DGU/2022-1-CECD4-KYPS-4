import cv2
import skeletonDetection as SD

protoFile = "2022-1-CECD4-KYPS-4\pre_processing\models\pose_deploy_linevec_faster_4_stages.prototxt"
weightFile = "2022-1-CECD4-KYPS-4\pre_processing\models\pose_iter_160000.caffemodel"
net = SD.load_model(protoFile, weightFile)

cap = cv2.VideoCapture(0)

print('width :%d, height : %d' % (cap.get(3), cap.get(4)))

while(True):
    ret, frame = cap.read()    # Read 결과와 frame
    
    frame = SD.resize_image(frame, 240, 180)
    
    if(ret) :
        resultImg, points = SD.detect(net, frame)

        for point in points:
            print(point)
        cv2.imshow("Output-Keypoints",resultImg)
        if cv2.waitKey(1) == ord('q'):
            break
        
        
cap.release()
cv2.destroyAllWindows()