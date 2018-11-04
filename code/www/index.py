from flask import render_template
import os
from code.slicer import slicer
from code.Detector import recognition
from picamera import PiCamera # picamera or pycamera?


class Index:
    def render_index(name=None):
        # the following will only be able to run on the raspberry pi
        image_path = "../../images"
        camera = PiCamera()
        camera.capture(image_path, "image.png")

        slicer.Slicer.slice(image_path)

        for image_path in os.listdir(image_path):
            print('Sending image' + image_path)
            # TODO send each image to be detected

        return render_template("index.html", name=name)
