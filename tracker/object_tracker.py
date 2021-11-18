'''
    File name         : object_tracking.py
    File Description  : Multi Object Tracker Using Kalman Filter
                        and Hungarian Algorithm
    Author            : Srini Ananthakrishnan
    Date created      : 07/14/2017
    Date last modified: 07/16/2017
    Python Version    : 2.7
'''

# Import python libraries
from cv2 import cv2
import copy
import time
from tracker.tracker import Tracker
# from kalman_filter_backup import KalmanFilter
from detector.yolo_detector import Detector


class ObjectTracker:

    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.detector = Detector('../model/yolov4.cfg', '../model/yolov4.weights', '../model/coco.names')
        self.tracker = Tracker(25, 60, 1000, 10)

    def tracking(self):
        track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                        (0, 255, 255), (255, 0, 255), (255, 127, 255),
                        (127, 0, 255), (127, 0, 127)]
        frame_array = []
        self.first = 0
        self.c = 0
        try:
            while True:
                ret, frame = self.cap.read()
                origin_frame = copy.copy(frame)
                bounding_box = self.detector.detection(frame)
                if len(bounding_box) > 0:
                    self.first = 1
                    self.tracker.Update(bounding_box, self.first)
                    print('NUM OF OBJECTS : ', len(self.tracker.tracks))
                    for i in range(len(self.tracker.tracks)):
                        if len(self.tracker.tracks[i].trace) > 1:
                            for j in range(len(self.tracker.tracks[i].trace) - 1):
                                # Draw trace line
                                x1 = self.tracker.tracks[i].trace[j][0][0]
                                y1 = self.tracker.tracks[i].trace[j][1][0]
                                x2 = self.tracker.tracks[i].trace[j + 1][0][0]
                                y2 = self.tracker.tracks[i].trace[j + 1][1][0]
                                clr = self.tracker.tracks[i].track_id % 9
                                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                         track_colors[clr], 2)
                elif self.first == 1:
                    self.tracker.Update(bounding_box, 0)
                    print('NUM OF OBJECTSno : ', len(self.tracker.tracks))
                    for i in range(len(self.tracker.tracks)):
                        if len(self.tracker.tracks[i].trace) > 1:
                            print('NUM OF OBJECTSnononono : ', len(self.tracker.tracks[i].trace), )
                            print('trace : ', self.tracker.tracks[i].trace[len(self.tracker.tracks[i].trace) - 1], )

                            for j in range(len(self.tracker.tracks[i].trace) - 1):
                                # Draw trace line
                                x1 = self.tracker.tracks[i].trace[j][0][0]
                                y1 = self.tracker.tracks[i].trace[j][1][0]
                                x2 = self.tracker.tracks[i].trace[j + 1][0][0]
                                y2 = self.tracker.tracks[i].trace[j + 1][1][0]
                                clr = self.tracker.tracks[i].track_id % 9

                                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                         track_colors[clr], 2)

                frame_array.append(frame)
                cv2.imshow('ss', frame)
                key = cv2.waitKey(1) & 0xFF

                # Exit
                if key == ord('q'):
                    break
                # Take screenshot
                if key == ord('s'):
                    cv2.imwrite('frame_{}.jpg'.format(time.time()), frame)

                self.c += 1
        except:
            print('video ended')
        finally:
            self.cap.release()
            cv2.destroyAllWindows()
