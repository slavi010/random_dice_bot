#################################################################################
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
# SOFTWARE.                                                                     #
#################################################################################
#
# Contributors :
# Copyright (c) 2020 slavi010 pro@slavi.dev
#


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

    # image = cv2.imread("../image/new_ui/empty_board.png")
    # print(image is not None)


    # mask = cv2.inRange(cv2.cvtColor(image, cv2.COLOR_BGR2HSV), (0, 0, 229), (160, 4, 241))
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)
    # image = cv2.bitwise_and(image, image, mask=mask)

    image[(image*255 < 42) | (image*255 > 81)] = 0
    ret, thresh = cv2.threshold(cv2.cvtColor(image.copy(),
                                             cv2.COLOR_RGB2GRAY),
                                162,
                                255,
                                cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    cv2.drawContours(image, contours, -1, (0, 225, 0), 3)
    cv2.imshow("show", image)
    cv2.waitKey(1000)

    max_area = 0
    max_boundRect = None
    for contour in contours:
        contour_poly = cv2.approxPolyDP(contour, 3, True)
        boundRect = cv2.boundingRect(contour_poly)
        if boundRect[2]*boundRect[3] > max_area:
            max_area = boundRect[2]*boundRect[3]
            max_boundRect = boundRect

    # point_x1 = max_boundRect[0] + max_boundRect[2]*0.16
    # point_y1 = max_boundRect[1] + max_boundRect[3]*0.22
    # point_x2 = max_boundRect[0] + max_boundRect[2]*0.85
    # point_y2 = max_boundRect[1] + max_boundRect[3]*0.765

    point_x1 = max_boundRect[0] + max_boundRect[2]*0.135
    point_y1 = max_boundRect[1] + max_boundRect[3]*0.205
    point_x2 = max_boundRect[0] + max_boundRect[2]*0.86
    point_y2 = max_boundRect[1] + max_boundRect[3]*0.760

    # image = cv2.rectangle(image, (int(max_boundRect[0]), int(max_boundRect[1])),
    #                       (int(max_boundRect[0]+max_boundRect[2]), int(max_boundRect[1]+max_boundRect[3])), (0, 255, 0), 2)
    # image[int(point_y1)][int(point_x1)] = (0, 0, 0)
    # image[int(point_y2)][int(point_x2)] = (0, 0, 0)
    # cv2.imshow("cv2", image)
    # cv2.waitKey(0)

    return int(x_1 + point_x1), int(y_1 + point_y1), int(x_1 + point_x2), int(y_1 + point_y2)


if __name__ == '__main__':
    grab_points_dice()
