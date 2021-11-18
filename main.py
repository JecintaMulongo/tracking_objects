from tracker.object_tracker import ObjectTracker

OB = ObjectTracker('/home/jecinta/Downloads/traffic.mp4')

OB.tracking()

# from cv2 import cv2
#
# from yolo_detector import Detector
# from video_tracking.videoasync import VideoCaptureProcess
#
# detector = Detector('../model/yolov4.cfg',
#                     '../model/yolov4.weights',
#                     '../model/coco.names')
#
# cap = cv2.VideoCapture('/home/jecinta/Downloads/f_.mp4')
#
# while True:
#
#     _, frame = cap.read()
#     if not _:
#         break
#
#     bb = detector.detection(frame)
#     print(bb)
#     for i in bb:
#         (x, y, w, h) = i[0], i[1], i[2], i[3]
#         class_name = i[-1]
#         cv2.rectangle(frame, (x, y), (w + x, h + y), (255, 255, 0), 4)
#
#         cv2.putText(frame, class_name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
#     # print(bb)
#     cv2.imshow('frame', frame)
#     cv2.waitKey(0)
