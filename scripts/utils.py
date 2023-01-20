from copy import copy
import cv2 as cv


def mouse_hover_callback(event, x, y, flags, param):
    global x_location
    global y_location
    global press
    if event == cv.EVENT_LBUTTONDOWN:
        press = True
    else:
        press = False
    if x != 0 or y != 0:
        x_location, y_location = x, y
    print(type(x_location))


def check_rectangles_collision(bbox1, bbox2):
    bbox2_points = ((bbox2[0], bbox2[1]), (bbox2[0]+bbox2[2], bbox2[1]), (bbox2[0], bbox2[1]+bbox2[3]),
                    (bbox2[0]+bbox2[2], bbox2[1]+bbox2[3]))
    for point in bbox2_points:
        if bbox1[0] < point[0] < bbox1[0]+bbox1[2] and bbox1[1] < point[1] < bbox1[1]+bbox1[3]:
            return True


def waste_time(frame, soldiers, time_to_waste):
    for i in range(int(time_to_waste*1000//20)):
        new_frame = copy(frame)
        soldiers.display_all_soldiers(frame)
        cv.imshow("game", new_frame)
        cv.waitKey(20)


def kill_with_mouse(event, x, y, flags, soldiers):
    if event == cv.EVENT_LBUTTONDOWN:
        soldiers.try_to_kill([x, y])
