import cv2
import numpy as np
import threading

webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

canvas = np.zeros((480,1280, 3), np.uint8)
cap1 = np.zeros((480,640, 3), np.uint8)
cap2 = np.zeros((480,640, 3), np.uint8)

mode = 0


class Swapper:
    def __init__(self, flat, cap):
        self.frame_count_float = 0
        self.frame_count = 0
        self.flat = flat
        self.cap = cap.copy().reshape((-1, 3))
        self.thread = threading.Thread(target=self.swap, args=())
        self.thread.start()

    def swap(self):
        while self.frame_count<len(self.flat):
            self.cap[self.frame_count] = self.flat[self.frame_count].copy()
            if self.frame_count < len(flat_cap2):
                self.frame_count_float += 0.1
                self.frame_count = int(self.frame_count_float)

    def read(self):
        frame = self.cap.copy().reshape((480,640,3))
        return frame

while True:
    ret, frame = webcam.read()

    if mode == 0:
        canvas[:, :640] = frame
    elif mode == 1:
        canvas[:, :640] = cap1
        canvas[:, 640:] = frame
    elif mode == 2:
        canvas[:, :640] = cap1
        canvas[:, 640:] = cap2
    elif mode == 3:
        canvas[:, :640] = cap1
        canvas[:, 640:] = cap2
        cap2 = swapper.read()
    cv2.imshow('lazy pixel', canvas)
    key = cv2.waitKey(1)
    if key == ord(' '):
        if mode < 3:
            if mode == 0:
                cap1 = frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                flat_gray = gray.flatten()
                index1 = np.argsort(flat_gray)
            elif mode == 1:
                cap2 = frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                flat_gray = gray.flatten()
                index2 = np.argsort(flat_gray)
            elif mode == 2:
                flat_cap1 = cap1.copy().reshape((-1, 3))
                flat_cap2 = cap2.copy().reshape((-1, 3))
                flat_cap2[index2] = flat_cap1[index1]
                swapper = Swapper(flat_cap2, cap2)

            mode += 1
        else:
            mode = 0
            cap1 = np.zeros((480, 640, 3), np.uint8)
            cap2 = np.zeros((480, 640, 3), np.uint8)
            canvas[:, 640:] = cap2

    if key == ord('q'):
        cv2.destroyAllWindows()
        webcam.release()
        break