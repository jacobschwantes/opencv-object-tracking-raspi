import cv2
import time


class VideoCamera(object):
    def __init__(self):
        self.vs = cv2.VideoCapture(0)
        self.last_detection = time.time()
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def get_object(self, classifier):
        found_objects = False
        result, frame = self.vs.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        # Check for object detection
        if len(objects) > 0:
            found_objects = True

        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return (frame, found_objects)
