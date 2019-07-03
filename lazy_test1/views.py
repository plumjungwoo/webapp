import threading

from django.shortcuts import render
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
from django.http import StreamingHttpResponse


# Create your views here.

def first_view(request):
    return render(request, 'lazy_test1/first_view.html', {})


def uimage(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(request, 'lazy_test1/uimage.html', {'form': form, 'uploaded_file_url': uploaded_file_url})
    else:
        form = UploadImageForm()
        return render(request, 'lazy_test1/uimage.html', {'form': form})


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


cam = VideoCamera()


def gen(cam):
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def livefe(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
