import os
import subprocess
import uiautomation as auto
import pyautogui
import time

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
    # os.startfile(r"C:\Program Files (x86)\EaseUS\RecExperts\bin\RecExperts.exe")
    subprocess.Popen([r"C:\Program Files (x86)\EaseUS\RecExperts\bin\RecExperts.exe"])
    ereMainWindow = auto.WindowControl(Name="EaseUS RecExperts", searchFromControl=auto.GetRootControl(), foundIndex=1)
    MyLibrary = ereMainWindow.CheckBoxControl(Name="My Library")
    StartRecording = ereMainWindow.CheckBoxControl(Name="Start Recording")
    EnterLicense = ereMainWindow.ButtonControl(Name="Enter License")
    Upgrade = ereMainWindow.ButtonControl(Name="Upgrade")
    Menu = ereMainWindow.CustomControl().ButtonControl(foundIndex=3)
    Close = ereMainWindow.CustomControl().ButtonControl(foundIndex=4)
    # Close = ereMainWindow.CustomControl().ButtonControl(foundIndex=5)
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

    # 折扣
    Discount_close = ereMainWindow.ButtonControl(Name="Skip This Discount")


class ScreenRecordWindow:
    # 初始化屏幕录制模块元素 ScreenRecordWindow
    ScreenRecordWindow = auto.WindowControl(Name="EaseUS RecExperts")
    ScreenRecord = ScreenRecordWindow.ButtonControl(foundIndex=11)
    ScreenShot = ScreenRecordWindow.ButtonControl(foundIndex=12)

class ErePlayerWindow:
    # 播放器模块元素
    ErePlayerWindow = auto.WindowControl(Name="EaseUS RecExperts")
    Close = ErePlayerWindow.CustomControl().ButtonControl(foundIndex=7)

class AudioRecordWindow:
    # 初始化音频录制模块元素 AudioRecordWindow
    AudioRecordWindow = auto.WindowControl(Name="EaseUS RecExperts")
    AudioRecord = AudioRecordWindow.ButtonControl(foundIndex=7)




if __name__ == '__main__':
    ere = EreMainWindow()
    ere.Discount_close.Click()






