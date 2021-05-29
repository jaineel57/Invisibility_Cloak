# Importing all the required libraries
import cv2 as cv
import numpy as np

# Intial function for calling the trackbar
def hello(x):
    print("")

# Intialization of the camera

cap = cv.VideoCapture(0)
bars = cv.namedWindow("bars")


cv.createTrackbar("upper_hue","bars",110,180,hello)
cv.createTrackbar("upper_saturation","bars",255,255,hello)
cv.createTrackbar("upper_value","bars",255,255,hello)
cv.createTrackbar("lower_hue","bars",68,180,hello)
cv.createTrackbar("lower_saturation","bars",55,255,hello)
cv.createTrackbar("lower_value","bars",54,255,hello)


# Capturing the intial frame for creation of background

while(True):
    cv.waitKey(1000)
    ret, init_frame = cap.read()
    # check if the frame is returned then break the loop
    if (ret):
        break


# Start capturing the magic
while(True):
    ret, frame = cap.read()
    inspect = cv.cvtColor(frame, cv.COLOR_BGR2HSV)


    # Getting the hsv values for masking the cloak
    upper_hue = cv.getTrackbarPos('upper_hue','bars')
    upper_saturation = cv.getTrackbarPos('upper_saturation','bars')
    upper_value = cv.getTrackbarPos('upper_value','bars')
    lower_hue = cv.getTrackbarPos('lower_hue', 'bars')
    lower_saturation = cv.getTrackbarPos('lower_saturation','bars')
    lower_value = cv.getTrackbarPos('lower_value','bars')

    # kernel to be used for dilation
    kernel = np.ones((3,3), np.uint8)


    upper_hsv = np.array([upper_hue,upper_saturation,upper_value])
    lower_hsv = np.array([lower_hue,lower_saturation,lower_value])

    mask = cv.inRange(inspect,lower_hsv,upper_hsv)
    mask = cv.medianBlur(mask,3)
    mask_inv = 255 - mask
    mask = cv.dilate(mask,kernel,5)


    # Mixing of frames in a combination to achieve the required frames

    b = frame[:,:,0]
    g = frame[:,:,1]
    r = frame[:,:,2]
    b = cv.bitwise_and(mask_inv,b)
    g = cv.bitwise_and(mask_inv,g)
    r = cv.bitwise_and(mask_inv,r)
    frame_inv = cv.merge((b,g,r))

    b = init_frame[:,:,0]
    g = init_frame[:,:,1]
    r = init_frame[:,:,2]
    b = cv.bitwise_and(b,mask)
    g = cv.bitwise_and(g,mask)
    r = cv.bitwise_and(r,mask)
    blanket_area = cv.merge((b,g,r))


    final = cv.bitwise_or(frame_inv, blanket_area)

    cv.imshow('Harrys Cloak',final)
    cv.imshow('Original', frame)

    if (cv.waitKey(3) == ord('q')):
        break


cv.destroyAllWindows()
cap.release()
