import sys
import numpy as np
import cv2
import matplotlib as mpl
import matplotlib.colors as mplc
import matplotlib.cm as mtpltcm
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import mediapipe as mp


# Set-ExecutionPolicy Unrestricted -Scope Process


cap = cv2.VideoCapture(1)

#initialize the colormap

colormap = mplc.ListedColormap([ # Dana Barret Aura-Rendering
       "#ae81d9","#be6450", "#35a055", "#2370c4", "#4aef76", "#87a5ff"
    ])


cNorm = mpl.colors.Normalize(vmin=0, vmax=255)
scalarMap = mtpltcm.ScalarMappable(norm=cNorm, cmap=colormap)

segmentor = SelfiSegmentation()

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    segmentated_img = segmentor.removeBG(frame, (0, 0, 0), cutThreshold=0.9)

    height, width = frame.shape[:2]

    # Our operations on the frame come here
    gray = cv2.cvtColor(segmentated_img, cv2.COLOR_BGR2GRAY)

    #assign colormap
    colors = scalarMap.to_rgba(gray, bytes=False)

    temp = cv2.resize(colors, (120, 120), interpolation=cv2.INTER_LINEAR)
    # Initialize output image
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

    blur = cv2.GaussianBlur(output, (15,5), 0)

    # Display the resulting frame
    cv2.imshow("window", blur)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


