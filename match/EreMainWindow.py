import uiautomation as auto
import subprocess
import pyautogui

def send_key(key):
    auto.SendKeys(key)

def get_screen_size():
    return pyautogui.size()

def drag(x1, y1, x2, y2):
    pyautogui.moveTo(x1, y1)
    pyautogui.dragTo(x2, y2, duration=1)


# 查找ere窗口
class EreMainWindow:


    # 初始化主界面的按钮元素 Start Recording
    # 启动ere
    subprocess.Popen([r"C:\Program Files (x86)\EaseUS\RecExperts\bin\RecExperts.exe"])
    ereMainWindow = auto.WindowControl(Name="EaseUS RecExperts")

    MyLibrary = ereMainWindow.CheckBoxControl(Name="My Library")
    MyLibraryRect = MyLibrary.BoundingRectangle

    StartRecording = ereMainWindow.CheckBoxControl(Name="Start Recording")
    EnterLicense = ereMainWindow.ButtonControl(Name="Enter License")
    Upgrade = ereMainWindow.ButtonControl(Name="Upgrade")
    Menu = ereMainWindow.CustomControl().ButtonControl(foundIndex=3)
    Min = ereMainWindow.CustomControl().ButtonControl(foundIndex=4)
    Close = ereMainWindow.CustomControl().ButtonControl(foundIndex=5)
    ScheduleRecording = ereMainWindow.ButtonControl(Name="Schedule Recording")
    More = ereMainWindow.ButtonControl(Name="More")

    # 初始化主界面的按钮元素 My Library
    Import = ereMainWindow.TabItemControl().ButtonControl(Name="Import")

    # 初始化主界面的按钮元素eremain
    FullScreen = ereMainWindow.ButtonControl(Name="MainScreenFunButton")
    Custom = ereMainWindow.ButtonControl(Name="Custom")
    Window = ereMainWindow.ButtonControl(Name="Window")
    Game = ereMainWindow.ButtonControl(Name="Game")
    Audio = ereMainWindow.ButtonControl(Name="Audio")
    Webcam = ereMainWindow.ButtonControl(Name="Webcam")


class ScreenRecordWindow:
    # 初始化屏幕录制模块元素 ScreenRecordWindow
    ScreenRecordWindow = auto.WindowControl(Name="EaseUS RecExperts")
    ScreenRecord = ScreenRecordWindow.ButtonControl(foundIndex=11)
    ScreenShot = ScreenRecordWindow.ButtonControl(foundIndex=12)

class ErePlayerWindow:
    # 播放器模块元素
    ErePlayerWindow = auto.WindowControl(Name="EaseUS RecExperts")
    Close = ErePlayerWindow.CustomControl().ButtonControl(foundIndex=8)

class AudioRecordWindow:
    # 初始化音频录制模块元素 AudioRecordWindow
    AudioRecordWindow = auto.WindowControl(Name="EaseUS RecExperts")
    AudioRecord = AudioRecordWindow.ButtonControl(foundIndex=7)





    # def high_light(self, rectangle):
    #     # 初始化 Windows API
    #     user32 = ctypes.windll.user32
    #     gdi32 = ctypes.windll.gdi32
    #
    #     # 创建画笔
    #     pen = gdi32.CreatePen(0, 2, 0x66ccff)  # 样式, 宽度, 颜色（BGR格式）
    #
    #     try:
    #         while True:
    #             # 获取控件位置
    #             rect = rectangle
    #             hdc = user32.GetDC(0)  # 获取屏幕设备上下文
    #
    #             # 绘制矩形
    #             gdi32.SelectObject(hdc, pen)
    #             gdi32.Rectangle(hdc, rect.left, rect.top, rect.right, rect.bottom)
    #
    #             # 释放资源
    #             user32.ReleaseDC(0, hdc)
    #             time.sleep(0.1)  # 控制刷新频率
    #
    #             # 清空绘制（通过覆盖白色矩形）
    #             hdc = user32.GetDC(0)
    #             gdi32.SelectObject(hdc, gdi32.GetStockObject(0))  # 白色画笔
    #             gdi32.Rectangle(hdc, rect.left, rect.top, rect.right, rect.bottom)
    #             user32.ReleaseDC(0, hdc)
    #
    #     except KeyboardInterrupt:
    #         gdi32.DeleteObject(pen)  # 清理画笔


if __name__ == '__main__':
    drag(0, 0, 1920, 1080)





