import sys
import numpy as np
import cv2
import matplotlib as mpl
import matplotlib.colors as mplc
import matplotlib.cm as mtpltcm
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import mediapipe as mp
from pygrabber.dshow_graph import FilterGraph


class VideoAnalyser:

    def __init__(self, videoCaptureDevice):
        print("Initialising...")

        # Set-ExecutionPolicy Unrestricted -Scope Process
        self.cap = cv2.VideoCapture(videoCaptureDevice)

        if not self.cap.read()[0]:
            print("\u001b[1mERROR: Invalid camera device, try a different index.")
            print("\033[0m")
            exit(1)

        # Dana Barret Aura-Rendering
        colormap = mplc.ListedColormap([ 
                "#ae81d9","#be6450", "#35a055", "#2370c4", "#4aef76", "#87a5ff"
                ])
        
        c_norm = mpl.colors.Normalize(vmin=0, vmax=255)
        self.scalarMap = mtpltcm.ScalarMappable(norm=c_norm, cmap=colormap)

        self.segmentor = SelfiSegmentation()

        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)


    def render_loop(self):
        print("Analysing spectral frequencies...")

        while (True):
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            if(not ret):
                print("\u001b[1mERROR: Could not get frame.")
                print("\033[0m")
                exit(1)

            segmentated_img = self.segmentor.removeBG(frame, (0, 0, 0), cutThreshold=0.9)

            height, width = frame.shape[:2]

            # Our operations on the frame come here
            gray = cv2.cvtColor(segmentated_img, cv2.COLOR_BGR2GRAY)

            # Assign colormap
            colors = self.scalarMap.to_rgba(gray, bytes=False)

            temp = cv2.resize(colors, (120, 120), interpolation=cv2.INTER_LINEAR)

            # Initialize output image
            output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

            blur = cv2.GaussianBlur(output, (15,5), 0)

            # Display the resulting frame
            cv2.imshow("window", blur)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def exit(self):
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()


# Returns the index and name of all connected camera devices
def get_available_cameras():

    devices = FilterGraph().get_input_devices()

    available_cameras = {}

    for device_index, device_name in enumerate(devices):
        available_cameras[device_index] = device_name

    return available_cameras


if __name__=="__main__":
    licensing_output = """Aura Video Analyser is a registered trademark of Ghostbusters
(c) Copyright 1984 Ghostbusters
All rights reserved
"""
    
    print("\033[92m")
    print(licensing_output)
    print(get_available_cameras())
    
    print("Enter camera index:")

    analyser = VideoAnalyser(int(input()))
    analyser.render_loop()
    analyser.exit()

    print("\033[0m")


