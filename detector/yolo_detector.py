import numpy as np
from cv2 import cv2


class Detector:

    def __init__(self, cfg_path, weight_path, coco_path, confidence=0.7, threshold=0.3):
        self.__confidence_ = confidence
        self.__threshold = threshold
        self.net = cv2.dnn.readNetFromDarknet(cfg_path, weight_path)
        layer = self.net.getLayerNames()
        self.layer = [layer[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.Label = open(coco_path).read().strip().split("\n")

    def detection(self, frame):

        H, W = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.layer)
        boxes, confidences, classIDs = [], [], []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > self.__confidence_:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (center_x, center_y, w, h) = box.astype("int")
                    x = int(center_x - (w / 2))
                    y = int(center_y - (h / 2))

                    # update our list of bounding box coordinates,
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.__confidence_, self.__threshold)

        # check if atlest one detection box exist
        bounding_boxes = []
        if len(idxs) > 0:
            for i in idxs.flatten():
                # get bounding box coordinates
                (x, y) = (int(boxes[i][0]), int(boxes[i][1]))
                (w, h) = (int(boxes[i][2]), int(boxes[i][3]))
                #bb = [x, y, w, h, float(confidences[i], ), self.Label[classIDs[i]]]
                bb = [x, y, w, h]
                cv2.rectangle(frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0))
                cv2.putText(frame, self.Label[classIDs[i]], (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 0))
                bounding_boxes.append(bb)
                return bounding_boxes
