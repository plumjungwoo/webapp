import cv2
import string
import base64
import random
import numpy as np
import threading
from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
from django.core.files.storage import FileSystemStorage


class Swapper:
    def __init__(self, flat, cap):
        self.frame_count_float = 0
        self.frame_count = 0
        self.flat = flat
        self.height = len(cap)
        self.width = len(cap[0])
        self.cap = cap.copy().reshape((-1, 3))
        self.thread = threading.Thread(target=self.swap, args=())
        self.thread.start()

    def swap(self):
        while self.frame_count < len(self.flat):
            self.cap[self.frame_count] = self.flat[self.frame_count].copy()
            if self.frame_count < len(self.flat):
                self.frame_count_float += 0.1
                self.frame_count = int(self.frame_count_float)

    def read(self):
        frame = self.cap.copy().reshape((self.height, self.width, 3))
        return frame


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(21, 0)
        (self.grabbed, self.frame) = self.video.read()

        self.height = len(self.frame)
        self.width = len(self.frame[0])
        self.canvas = np.zeros((self.height, self.width * 2, 3), np.uint8)
        self.cap1 = np.zeros((self.height, self.width, 3), np.uint8)
        self.cap2 = np.zeros((self.height, self.width, 3), np.uint8)

        self.mode = 0

        self.random_id = self.randstr()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def randstr(self, string_length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))

    def get_frame(self):
        ret, jpeg = cv2.imencode('.jpg', self.canvas)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            if self.mode == 0:
                self.canvas[:, :self.width] = self.frame
            elif self.mode == 1:
                self.canvas[:, :self.width] = self.cap1
                self.canvas[:, self.width:] = self.frame
            elif self.mode == 2:
                self.canvas[:, :self.width] = self.cap1
                self.canvas[:, self.width:] = self.cap2
            elif self.mode == 3:
                self.canvas[:, :self.width] = self.cap1
                self.canvas[:, self.width:] = self.cap2
                self.cap2 = self.swapper.read()

    def click(self):
        if self.mode < 3:
            if self.mode == 0:
                self.cap1 = self.frame
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                flat_gray = gray.flatten()
                self.index1 = np.argsort(flat_gray)
            elif self.mode == 1:
                self.cap2 = self.frame
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                flat_gray = gray.flatten()
                self.index2 = np.argsort(flat_gray)
            elif self.mode == 2:
                flat_cap1 = self.cap1.copy().reshape((-1, 3))
                flat_cap2 = self.cap2.copy().reshape((-1, 3))
                flat_cap2[self.index2] = flat_cap1[self.index1]
                self.swapper = Swapper(flat_cap2, self.cap2)

            self.mode += 1
        else:
            self.mode = 0
            self.cap1 = np.zeros((self.height, self.width, 3), np.uint8)
            self.cap2 = np.zeros((self.height, self.width, 3), np.uint8)
            self.canvas[:, self.width:] = self.cap2


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


cam = VideoCamera()

def liveStream(request):
    global cam
    try:
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except :
        pass

def index(request):
    global cam
    if request.method == 'POST':
        cam.click()
    return render(request, 'lazy_test1/uimage.html', {})