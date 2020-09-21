# Untitled - By: boris - Сб ноя 16 2019

import sensor, image, time
from math import sqrt, atan2
from pyb import UART
EXPOSURE_TIME_SCALE = 1.0

txrx = UART(3,115200, timeout_char = 1)
txrx.init(115200, bits=8, parity=None, stop=1,timeout_char = 1)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(True)
sensor.set_auto_exposure(True)
sensor.set_auto_whitebal(True)
sensor.skip_frames(time = 500)

sensor.set_auto_whitebal(True)
sensor.set_auto_gain(False)
sensor.set_auto_exposure(False)
current_exposure_time_in_microseconds=  sensor.get_exposure_us()
sensor.set_auto_exposure(False, \
    exposure_us = int(current_exposure_time_in_microseconds* EXPOSURE_TIME_SCALE))
sensor.skip_frames(time = 2000)

clock = time.clock()

threshold_blue=(0, 49, 10, 127, -55, -10)
threshold_yellow=(65, 88, 20, 52, 32, 127)


def realDistance(x):
    fSign = 1
    if x<0:
        xAbs = x*-1
        fSign = -1
    else:
        xAbs = x
    if(0<=xAbs and xAbs<46):
        xOne = 0
        xTwo = 46
        yOne = 0
        yTwo = 16
    elif(46<=xAbs and xAbs<56):
        xOne = 46
        xTwo = 56
        yOne = 16
        yTwo = 20
    elif(56<=xAbs and xAbs<65):
        xOne = 56
        xTwo = 65
        yOne = 20
        yTwo = 25
    elif(65<=xAbs and xAbs<74):
        xOne = 65
        xTwo = 74
        yOne = 25
        yTwo = 30
    elif(74<=xAbs and xAbs<80):
        xOne = 74
        xTwo = 80
        yOne = 30
        yTwo = 35
    elif(80<=xAbs and xAbs<85):
        xOne = 80
        xTwo = 85
        yOne = 35
        yTwo = 40
    elif(85<=xAbs and xAbs<90):
        xOne = 85
        xTwo = 90
        yOne = 40
        yTwo = 45
    elif(90<=xAbs and xAbs<95):
        xOne = 90
        xTwo = 95
        yOne = 45
        yTwo = 50
    elif(95<=xAbs and xAbs<100):
        xOne = 95
        xTwo = 100
        yOne = 50
        yTwo = 60
    elif(100<=xAbs and xAbs<105):
        xOne = 100
        xTwo = 105
        yOne = 60
        yTwo = 75
    elif(105<=xAbs and xAbs<108):
        xOne = 105
        xTwo = 108
        yOne = 75
        yTwo = 90
    elif(108<=xAbs and xAbs<113):
        xOne = 108
        xTwo = 113
        yOne = 90
        yTwo = 110
    elif(113<=xAbs and xAbs<=117):
        xOne = 113
        xTwo = 117
        yOne = 110
        yTwo = 130
    return (((xAbs-xOne)*(yTwo-yOne))/(xTwo-xOne) + yOne)*fSign

while(True):
    clock.tick()
    img = sensor.snapshot()
    blobsPreviousMas = 0
    biggestBlueBlob = 0
    count =0
    blobsBlue=[]
    for blueBlob in img.find_blobs([threshold_blue],roi=(0,0,319,239), pixels_threshold=200, area_threshold=200, merge=True):
        blobsBlue.append(blueBlob)
        if(blueBlob.area() > blobsPreviousMas):
            biggestBlueBlob = count
            blobsPreviosMas =blueBlob.area()
        count+=1
    try:
        img.draw_rectangle(blobsBlue[biggestBlueBlob].rect())
    except: pass
    PreviousMas = 0
    biggestYellowBlob = 0
    count =0
    blobsYellow=[]
    for yellowBlob in img.find_blobs([threshold_yellow],roi=(0,0,319,239), pixels_threshold=200, area_threshold=200, merge=True):
        blobsYellow.append(yellowBlob)
    try:
        img.draw_rectangle(blobsYellow[biggestYellowBlob].rect())
        img.draw_cross(blobsYellow[biggestYellowBlob].cx(),blobsYellow[biggestYellowBlob].cy(), 6)
    except: pass
    maxLeft = 320
    maxRight = 0
    count = 0
    indL = 0
    indR = 0
    centerY = 0
    centerX = 0

    for blooo, i in enumerate(blobsYellow):
        if (maxLeft > blobsYellow[blooo].x()):
            maxLeft = blobsYellow[blooo].x()
            indL = count
        if (maxRight < blobsYellow[blooo].cx() + blobsYellow[blooo].cx() - blobsYellow[blooo].x()):
            maxRight = blobsYellow[blooo].cx() + blobsYellow[blooo].cx() - blobsYellow[blooo].x()
            indR = count
        count+=1
    try:
        centerY = (blobsYellow[indL].cy() + blobsYellow[indR].cy()) // 2
        centerX = (maxLeft + maxRight) // 2
        GLX = realDistance(- centerX + 159)
        GLY = realDistance(-centerY + 112)
        angle = atan2(GLX, GLY)
        angle = (angle*57)//1
        workAngle = 0
        if angle > 0:
            workAngle = angle - 90
        else:
            workAngle = angle + 90
        line_ = 0
        lineAngle = (atan2(-GLY, 61)*57)//1
        if (workAngle > 0 and workAngle < lineAngle + 20) or (angle < 0 and workAngle > -(lineAngle+20)):
            line_ = 1
        print("Line: ")
        print(line_)
        txrx.write(str(line_))
        print("LINEAngle:")
        print(lineAngle)
        print(workAngle)
        img.draw_cross(centerX,centerY)
        img.draw_line(173,112,centerX,centerY)
        txrx.write("*")
    except: pass
    gray = img
    img.draw_circle(163,95,10)
