import cv2
import win32api
import win32gui
import time
from ImageBase import utils
from ImageBase.Size import Size, Point, Rect
from constanct import SM_CXVIRTUALSCREEN, SM_CYVIRTUALSCREEN
from CapMethod.Bitblt import BitBlt
from typing import Dict, Union, Tuple, List
from pywinauto import mouse, keyboard
from match import sift



class Win(object):
    def __init__(self, handle_title: str = None, handle_class: str = None):
        if handle_title:
            self._hwnd = self.find_window(hwnd_title=handle_title)
            self._window_size = Size(win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN),  # 全屏幕尺寸大小
                                 win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN))
            print(f'设备分辨率:{self._window_size}, 窗口所用句柄: {self._hwnd}')

        self.mouse = mouse
        self.keyboard = keyboard

    @staticmethod
    def find_window(hwnd_class: str = None, hwnd_title: str = None) -> int:
        """
        根据窗口名或窗口类名获取对应窗口句柄

        Args:
            hwnd_class: 窗口类名
            hwnd_title: 窗口名

        Returns:
            窗口句柄
        """
        return win32gui.FindWindow(hwnd_class, hwnd_title)

    @property
    def rect(self) -> Rect:
        """
        获取窗口客户端区域当前所在屏幕的位置

        Returns:
            窗口的位置(以全屏左上角开始为原点的坐标)
        """
        client_rect = win32gui.GetClientRect(self._hwnd)
        point = win32gui.ScreenToClient(self._hwnd, (0, 0))
        rect = Rect(x=abs(point[0]), y=abs(point[1]), width=client_rect[2], height=client_rect[3])
        return rect

    def screenshot(self):
        screenshot_size = Size(self.rect.width, self.rect.height)
        img = BitBlt(hwnd=self._hwnd, border=[0,0], screenshot_size=screenshot_size).screenshot()
        return img

    def _window_pos2screen_pos(self, pos: Point):
        """
        转换相对坐标为屏幕的绝对坐标

        Args:
            pos: 需要转换的坐标

        Returns:
            Point
        """
        windowpos = self.rect.tl
        pos = pos + windowpos
        return pos

    def click(self, point: Union[Tuple[int, int], List, Point], duration: Union[float, int, None] = 0.01,
              button: str = 'left'):
        """
        点击连接窗口的指定位置 ps:相对坐标,以连接的句柄窗口左上角为原点

        Args:
            point: 需要点击的坐标
            duration: 延迟
            button: 左右键 left/right

        Returns:
            None
        """

        if isinstance(point, (tuple, list)):
            point = Point(x=point[0], y=point[1])

        point = self._window_pos2screen_pos(point)
        print('change',point)

        self.mouse.press(button=button, coords=(point.x, point.y))
        time.sleep(duration)
        self.mouse.release(button=button, coords=(point.x, point.y))

if __name__ == '__main__':
    ere = Win(handle_title='EaseUsMainWindow')
    print(ere.rect)
    a = ere.screenshot()
    b = utils.read_images(r'D:\pyproject\winAuto_shu\pythonProject\test\screen.png')
    result, corners, matches = sift.sift_feature_matching_with_box(a, b)
    cv2.imshow('Matched and Boxed Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print(c)
