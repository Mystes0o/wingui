import win32api
import win32con
import win32gui
import time
from ImageBase import utils
from ImageBase.Size import Size, Point, Rect
from constanct import SM_CXVIRTUALSCREEN, SM_CYVIRTUALSCREEN
from CapMethod.Bitblt import BitBlt
from CapMethod.windowsGraphicsCapture import WindowGraphicsCapture
from typing import Union, Tuple, List
from pywinauto import mouse, keyboard
from match import orb, ocr
from loguru import logger


class Win(object):
    def __init__(self, handle_title: str = None, handle_class: str = None):
        if handle_title:
            self._hwnd = self.find_window(hwnd_title=handle_title)
            self._window_size = Size(win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN),  # 全屏幕尺寸大小
                                     win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN))
            logger.info(f'设备分辨率:{self._window_size}, 窗口所用句柄: {self._hwnd}')

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
        try:
            img = WindowGraphicsCapture(hwnd=self._hwnd).screenshot()
        except WindowsError:
            logger.error('WindowGraphicsCapture 截图失败，尝试使用 Bitblt 截图')
            img = BitBlt(hwnd=self._hwnd, border=[0, 0], screenshot_size=screenshot_size).screenshot()
        return img

    def draw_highlight(self, color=win32api.RGB(255, 255, 255), thickness=5):
        hdc = win32gui.GetWindowDC(self._hwnd)
        left, top, right, bottom = 100, 100, 200, 200
        brush = win32gui.CreateSolidBrush(color)
        pen = win32gui.CreatePen(win32con.PS_SOLID, thickness, color)
        win32gui.SelectObject(hdc, brush)
        win32gui.SelectObject(hdc, pen)

        # 绘制边框
        win32gui.Rectangle(hdc, left, top, right, bottom)
        win32gui.DeleteObject(brush)
        win32gui.DeleteObject(pen)
        win32gui.ReleaseDC(self._hwnd, hdc)

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

    def click_pic(self, template, duration: Union[float, int, None] = 0.03,
              button: str = 'left'):
        """
        点击连接窗口的指定位置 ps:相对坐标,以连接的句柄窗口左上角为原点

        Args:
            template: 需要点击的图片
            duration: 延迟
            button: 左右键 left/right

        Returns:
            None
        """
        try:
            point = orb.match_descriptor(template, self.screenshot())
        except WindowsError:
            point = Point(0, 0)

        if isinstance(point, (tuple, list)):
            point = Point(x=point[0], y=point[1])

        point = self._window_pos2screen_pos(point)
        logger.info(f'点击位置:{point}')

        self.mouse.press(coords=(point.x, point.y), button=button)
        time.sleep(duration)
        self.mouse.release(coords=(point.x, point.y), button=button)

    def click_text(self, text: str, duration: Union[float, int, None] = 0.03,button: str = 'left'):
        point = ocr.ocr_match(self.screenshot(), text)[0]
        point = self._window_pos2screen_pos(point)
        logger.info(f'点击位置:{point}')
        self.mouse.press(coords=(point.x, point.y), button=button)
        time.sleep(duration)
        self.mouse.release(coords=(point.x, point.y), button=button)






if __name__ == '__main__':
    ereMain = Win(handle_title='EaseUs RecExperts')
    ereMain.click_text('REC')
    # time.sleep(300)
