from threading import Thread
import numpy as np
import cv2
import time
import math


class Window(Thread):
    def __init__(self, trackers):
        """
        This class defines the perception of the robot and implements the various detection and tracking algorithms needed
        :type name: Window
        """
        self.img = np.zeros((1080, 1920, 3), dtype=np.int32)
        self.first_frame = np.zeros((1080, 1920, 3), dtype=np.int32)
        self.trackers = trackers
        self.tracker_roi = (0, 0, 0, 0)
        self.tracking_success = False

    def detect_body_haar(self):
        """
        Summary line.
        implement fullbody detection with an haarcascade detector

        Parameters:
        self.img

        Returns:
        draw a box around the detected object, if a person is detected on self.img
        """
        fullbody_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        bodies = fullbody_cascade.detectMultiScale(gray)
        for (x, y, w, h) in bodies:
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (255, 0, 0), 10)

        return bodies

    def detect_body_yolo(self):
        """

        :return:
        """

        def process_image(img):
            """Resize, reduce and expand image.

            # Argument:
                img: original image.

            # Returns
                image: ndarray(64, 64, 3), processed image.
            """
            image = cv2.resize(img, (1080, 1920),
                               interpolation=cv2.INTER_CUBIC)
            image = np.array(image, dtype='float32')
            image /= 255.
            image = np.expand_dims(image, axis=0)

            return image

        def get_classes(file):
            """Get classes name.

            # Argument:
                file: classes name for database.

            # Returns
                class_names: List, classes name.

            """
            with open(file) as f:
                class_names = f.readlines()
            class_names = [c.strip() for c in class_names]

            return class_names

        def draw(image, boxes, scores, classes, all_classes):
            for box, score, cl in zip(boxes, scores, classes):
                x, y, w, h = box

                top = max(0, np.floor(x + 0.5).astype(int))
                left = max(0, np.floor(y + 0.5).astype(int))
                right = min(image.shape[1], np.floor(x + w + 0.5).astype(int))
                bottom = min(image.shape[0], np.floor(y + h + 0.5).astype(int))

                cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
                cv2.putText(image, '{0} {1:.2f}'.format(all_classes[cl], score),
                            (top, left - 6),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 0, 255), 1,
                            cv2.LINE_AA)

                print('class: {0}, score: {1:.2f}'.format(all_classes[cl], score))
                print('box coordinate x,y,w,h: {0}'.format(box))

            print()

        def detect_image(image, yolo, all_classes):
            """Use yolo v3 to detect images.

            # Argument:
                image: original image.
                yolo: YOLO, yolo model.
                all_classes: all classes name.

            # Returns:
                image: processed image.
            """
            pimage = process_image(image)

            start = time.time()
            boxes, classes, scores = yolo.predict(pimage, image.shape)
            end = time.time()

            print('time: {0:.2f}s'.format(end - start))

            if boxes is not None:
                draw(image, boxes, scores, classes, all_classes)

            return image

        yolo = YOLO(0.3, 0.5)
        file = 'data/coco_classes.txt'
        all_classes = get_classes(file)

        # TODO get the boxes instead of directly drawing on the image
        self.img = detect_image(self.img, yolo, all_classes)

    def init_tracker(self, roi):
        """
        Summary line.
        used on the first frame to draw a box around the object to be tracked

        Parameters:
        self.first frame is used to define the ROI that initializes tracking

        Returns:
        set the new value for self.tracker_roi and self.tracker
        """

        roi = tuple(map(int, roi))
        tracker = cv2.TrackerMedianFlow_create
        self.trackers.add(tracker, self.img, roi)

    def tracker_display(self):
        """
        Summary line.
        implement tracking

        Parameters:
        the current value of self.tracker stored from the previous frame is used

        Returns:
        draw a box on self.img to keep track of the moving object. the value of self.roi is also modified and stored
        """
        (success, boxes) = self.trackers.update(self.img)

        for box in boxes:
            (x, y, w, h) = tuple(map(int, box))

        if success:
            p1 = (x,y)
            p2 = (x+w, y+h)
            cv2.rectangle((self.img, p1, p2, (0,255, 0), 3))
            self.tracking_success = True

        else:
            self.tracking_success = False


    def get_frame(self):
        """
        Summary line.
        simple accessor
        """
        return self.img

    def set_frame(self, frame):
        """
        Summary line.
        accessor used on every image received in UdpSocket except the first one to store the current frame in the
        window object for further treatment

        Parameters:
        the value of the current frame, of type np.array and normal shape is (1080, 1920, 3)

        Returns:
        set the value of self.img with value passed in argument

        """
        self.img = frame

    def set_first_frame(self, first_frame):
        """
        Summary line.
        accessor only used once in UdpSocket to set the first frame coming through the server

        Parameters:
        the value of the first frame, of type np.array and normal shape is (1080, 1920, 3)

        Returns:
        set the value of self.first_frame with value passsed in argument
        """
        self.first_frame = first_frame

    def is_tracking_success(self):
        return self.tracking_success


"""
    def __del__(self):
        cv2.destroyWindow(self.win_name)
        print("destructor called")
"""
