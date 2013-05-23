#!/bin/python

import opencv
import cv

def repeat():
    print "getting frame"
    frame = cv.QueryFrame(capture)
    print "Frame gotten"
    cv.ShowImage("w1", frame)
    print "Shown image"

cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(0)

while True:
    repeat()
