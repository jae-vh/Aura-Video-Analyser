import sys

import cv2
import matplotlib as mpl
import matplotlib.colors as mplc
import matplotlib.cm as mtpltcm
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation

if 'win32' in sys.platform:
    from pygrabber.dshow_graph import FilterGraph

elif sys.platform.startswith('linux'):
    from screeninfo import get_monitors
    import pyudev

else:
    raise RuntimeError("\u001b[1mUnsupported operating system.\033[0m")    



# Dana Barret Aura-Rendering
COLORMAP = mplc.ListedColormap([ 
        "#ae81d9",
        "#be6450",
        "#35a055",
        "#2370c4",
        "#4aef76",
        "#87a5ff"
        ])

# Fictional Ghostbusters license :D
LICENSE = """Aura Video-Analyser is a registered trademark of Ghostbusters
(c) Copyright 1984 Ghostbusters
All rights reserved
"""



class VideoAnalyser:

    def __init__(self, camera_index):
        print("Initialising...")

        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_ANY)

        if not self.cap.isOpened():
            raise RuntimeError("\u001b[1mInvalid camera device, try a different number.\033[0m")
        
        c_norm = mpl.colors.Normalize(vmin=0, vmax=255)
        self.scalar_map = mtpltcm.ScalarMappable(norm=c_norm, cmap=COLORMAP)

        self.segmentor = SelfiSegmentation()

        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        self._scaling_setup()


    def _scaling_setup(self):
        """Provides setup functionality for ensuring image is scaled to screen"""

        # Get the window size 
        if 'win32' in sys.platform:
            self.window_width = cv2.getWindowImageRect("window")[2]
            self.window_height = cv2.getWindowImageRect("window")[3]

        # Get the window size (getWindowImageRect does not work as expected on Linux)
        elif sys.platform.startswith('linux'):
            monitor = get_monitors()[0]
            self.window_width = monitor.width
            self.window_height = monitor.height

        ret, frame = self.cap.read()        
        height, width = frame.shape[:2]

        # This is so we can scale the image to screen size while maintaining aspect ratio
        scale = min(self.window_width / width, self.window_height / height)

        self.new_image_width = int(width * scale)
        self.new_image_height = int(height * scale)

        x = int((self.window_width - self.new_image_width) // 2)
        y = int((self.window_height - self.new_image_height) // 2)

        # Used to move the scaled image to center of screen
        self.translation_matrix = np.float32([[1, 0, x], [0, 1, y]])


    def render_loop(self):
        """Continuously capture, process, and display aura-rendered video frames."""

        print("Analysing spectral frequencies...")

        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            if not ret:
                raise RuntimeError("\u001b[1mCould not get frame\033[0m")

            segmented_img = self.segmentor.removeBG(frame, (0, 0, 0), cutThreshold=0.9)

            # Our operations on the frame come here
            gray = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)

            # Assign colormap
            colors = self.scalar_map.to_rgba(gray, bytes=False)

            small_image = cv2.resize(colors, (120, 120), interpolation=cv2.INTER_LINEAR)

            # Scale image to screen size
            scaled_image = cv2.resize(small_image, (self.new_image_width, self.new_image_height), interpolation=cv2.INTER_AREA)

            translated_image = cv2.warpAffine(scaled_image, self.translation_matrix, (self.window_width, self.window_height))

            # Display the resulting frame
            cv2.imshow("window", translated_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                return


    def close(self):
        """Releases camera and closes OpenCV window"""
        print("Shutdown sequence initiated...")

        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()


if 'win32' in sys.platform:
    def get_available_cameras():
        """Prints the index and name of all connected camera devices"""

        devices = FilterGraph().get_input_devices()
        print(dict(enumerate(devices)))

elif sys.platform.startswith('linux'):
    def get_available_cameras():
        """Prints the index and name of all connected camera devices"""

        context = pyudev.Context()

        index = 0
        previous_device_name = None

        camera_devices = context.list_devices(subsystem="video4linux")

        for device in camera_devices:
            device_name = device.get("ID_MODEL")

            # Ensures the same device isn't printed twice (due to meta files)            
            if device_name == previous_device_name:
                continue

            previous_device_name = device_name

            print(f"{index}: {device_name}")

            index += 1
        
        if index == 0:
            raise RuntimeError("\u001b[1mNo camera devices found\033[0m")



if __name__ == "__main__":    
    print("\033[92m")
    print(LICENSE)
    print("Camera devices: ")
    get_available_cameras()
    
    camera_index = int(input("Enter camera number: "))
    analyser = VideoAnalyser(camera_index)

    try:
        analyser.render_loop()
    finally:
        analyser.close()

    print("\033[0m")