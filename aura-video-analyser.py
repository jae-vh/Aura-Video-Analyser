import cv2
import matplotlib as mpl
import matplotlib.colors as mplc
import matplotlib.cm as mtpltcm
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from pygrabber.dshow_graph import FilterGraph


class VideoAnalyser:

    def __init__(self, camera_index):
        print("Initialising...")

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("\u001b[1mInvalid camera device, try a different index.\033[0m")

        # Dana Barret Aura-Rendering
        COLORMAP = mplc.ListedColormap([ 
                "#ae81d9","#be6450", "#35a055", "#2370c4", "#4aef76", "#87a5ff"
                ])
        
        c_norm = mpl.colors.Normalize(vmin=0, vmax=255)
        self.scalarMap = mtpltcm.ScalarMappable(norm=c_norm, cmap=COLORMAP)

        self.segmentor = SelfiSegmentation()

        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


    def render_loop(self):
        """Continuously capture, process, and display aura-rendered video frames."""

        print("Analysing spectral frequencies...")

        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            if not ret:
                raise RuntimeError("\u001b[1mCould not get frame\033[0m")

            segmented_img = self.segmentor.removeBG(frame, (0, 0, 0), cutThreshold=0.9)

            height, width = frame.shape[:2]

            # Our operations on the frame come here
            gray = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)

            # Assign colormap
            colors = self.scalarMap.to_rgba(gray, bytes=False)

            small_image = cv2.resize(colors, (120, 120), interpolation=cv2.INTER_LINEAR)

            # Initialize output image
            scaled_image = cv2.resize(small_image, (width, height), interpolation=cv2.INTER_NEAREST)

            blur = cv2.GaussianBlur(scaled_image, (15,5), 0)

            # Display the resulting frame
            cv2.imshow("window", blur)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                return

    def close(self):
        """Releases camera and closes OpenCV window."""

        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()


def get_available_cameras():
    """Returns the index and name of all connected camera devices"""

    devices = FilterGraph().get_input_devices()

    return dict(enumerate(devices))


if __name__ == "__main__":
    LICENSE = """Aura Video Analyser is a registered trademark of Ghostbusters
(c) Copyright 1984 Ghostbusters
All rights reserved
"""
    
    print("\033[92m")
    print(LICENSE)
    print(get_available_cameras())
    
    camera_index = int(input("Enter camera index: "))
    analyser = VideoAnalyser(camera_index)

    try:
        analyser.render_loop()
    finally:
        analyser.close()

    print("\033[0m")


