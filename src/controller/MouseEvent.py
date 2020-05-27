from time import sleep

import cv2
from pynput import mouse

from src.model import Plateau


class MyException(Exception): pass


def get_next_click_mouse():
    def on_click(x, y, button, pressed):
        if button == mouse.Button.left:
            raise MyException(x, y, button, pressed)

    # Collect events until released
    with mouse.Listener(
            on_click=on_click) as listener:
        try:
            listener.join()
        except MyException as e:
            return e.args[0], e.args[1], e.args[2], e.args[3]
    return None, None, None, None


def grab_points_dice():
    x_1, y_1, _, _ = get_next_click_mouse()
    sleep(0.5)
    x_2, y_2, _, _ = get_next_click_mouse()

    image = Plateau.grab_image()[y_1:y_2, x_1:x_2]

    # image = cv2.imread("image/empty_board.png")

    mask = cv2.inRange(cv2.cvtColor(image, cv2.COLOR_BGR2HSV), (0, 0, 0), (250, 250, 250))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    image = cv2.bitwise_and(image, image, mask=mask)

    ret, thresh = cv2.threshold(cv2.cvtColor(image.copy(),
                                             cv2.COLOR_BGR2GRAY),
                                20,
                                255,
                                cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    max_area = 0
    max_boundRect = None
    for contour in contours:
        contour_poly = cv2.approxPolyDP(contour, 3, True)
        boundRect = cv2.boundingRect(contour_poly)
        if boundRect[2]*boundRect[3] > max_area:
            max_area = boundRect[2]*boundRect[3]
            max_boundRect = boundRect

    point_x1 = max_boundRect[0] + max_boundRect[2]*0.15
    point_y1 = max_boundRect[1] + max_boundRect[3]*0.22
    point_x2 = max_boundRect[0] + max_boundRect[2]*0.853
    point_y2 = max_boundRect[1] + max_boundRect[3]*0.765

    # image = cv2.rectangle(image, (int(max_boundRect[0]), int(max_boundRect[1])),
    #                       (int(max_boundRect[0]+max_boundRect[2]), int(max_boundRect[1]+max_boundRect[3])), (0, 255, 0), 2)
    # image[int(point_y1)][int(point_x1)] = (0, 0, 0)
    # image[int(point_y2)][int(point_x2)] = (0, 0, 0)
    # cv2.imshow("cv2", image)
    # cv2.waitKey(0)

    return int(x_1 + point_x1), int(y_1 + point_y1), int(x_1 + point_x2), int(y_1 + point_y2)
