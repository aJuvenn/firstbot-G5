import time
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
### MAGIC NUMBERS ###

# define range of yellow-green stripes
lower_spec = np.array([20,95,85])
upper_spec = np.array([50,255,220])


# define range of black color in HSV
lower_black = np.array([0,0,0])
upper_black = np.array([120,140,80])

# define range of blue color in HSV
lower_blue = np.array([100,55,55])
upper_blue = np.array([125,255,255])

# define range of red color in HSV
lower_red = np.array([0,40,40])
upper_red = np.array([5,240,255])

# define range of orange color in HSV
lower_orange = np.array([10,40,40])
upper_orange = np.array([20,240,250])

    
    
relative_position = 0.
    
def get_and_analyse_frame(color):
    
    # Numbers of rows
    #global_start = time.time()
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
   # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    #mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Threshold the HSV image to get only red colors
    if color == 'red':
        mask = cv2.inRange(hsv, lower_red, upper_red)
    elif color == 'black':
        mask = cv2.inRange(hsv, lower_black, upper_black)
    else : 
        mask = cv2.inRange(hsv, lower_red, upper_red)
    # Threshold the HSV image to get only orange colors
    #mask = cv2.inRange(hsv, lower_orange, upper_orange)
    
    # Taking a matrix of size 5 as the kernel 
    kernel = np.ones((5,5), np.uint8)   
    # The first parameter is the original image, 
    # kernel is the matrix with which image is  
    # convolved and third parameter is the number  
    # of iterations, which will determine how much  
    # you want to erode/dilate a given image.
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask=closing)
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur for better edge detection
    #blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
    ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #thresh  = cv2.bitwise_not(thresh)

    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_NONE)
    # Find the biggest contour (if detected)
    if len(contours) > 0:
        try : 
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            cx = float(M['m10'])/float(M['m00'])
            cy = float(M['m01'])/float(M['m00'])
            #cv2.circle(frame,(cx,cy), 3, (0,0,255), -1)
            #cv2.drawContours(frame, c, -1, (0,255,0), 1)
            #rows,cols = frame.shape[:2]
            #[vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
            #lefty = int((-x*vy/vx) + y)
            #righty = int(((cols-x)*vy/vx)+y)
            #cv2.line(frame,(cols-1,righty),(0,lefty),(0,255,0),2)
            #print('sizeX=%s'% frame.shape[0])
            #print('sizeY=%s'% frame.shape[1])
            global relative_position
            relative_position = cx/float(frame.shape[1])-0.5
            return relative_position
       #     print(relative_position)#return relative_position
        except :
            #print('No contour')
            return relative_position
            
    #print('WTF')
    return relative_position
    #cv2.imshow('frame',frame)
    #cv2.imshow('thresh',thresh)
    #cv2.imshow('thresh_dilation',img_dilation)
    #global_end = time.time()
    #complete_loop = global_end - global_start
    #print(complete_loop)
    #cv2.imshow("frame",frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
     #   break

def spec_line_detection():
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_spec, upper_spec)
    mean = cv2.mean(mask)[0]
    if mean>5:
        return True
    else :
        return False

def can_start():
    return cap.isOpened()
