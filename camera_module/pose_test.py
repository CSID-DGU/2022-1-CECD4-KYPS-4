import cv2
import mediapipe as mp
import time
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 프레임 카운터
fCount = 1

cap = cv2.VideoCapture(0)
start_time = time.time()

# fps 확인
fps = cap.get(cv2.CAP_PROP_FPS)

with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        
        success, image = cap.read()
        if not success:
            print("카메라를 찾을 수 없습니다.")
            continue

        # 이미지 작성
        image.flags.writeable = False   
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # 프레임 별 화면 저장
        if((time.time() - start_time)  / fCount >= 1):
            # print(int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
            cv2.imwrite("./frame/frame%d.jpg" % fCount, image)
            print('Saved! Frame num : ', fCount)
            fCount += 1
            
            print(results.pose_world_landmarks)

        # 포즈 오버레이
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        # 좌우반전
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))  
        # time.sleep(1)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()