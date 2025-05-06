import uiautomation as auto


# 查找ere窗口
class EreMainWindow:
    # 初始化主界面的按钮元素 Start Recording
    ereMainWindow = auto.WindowControl(Name="EaseUS RecExperts")
    MyLibrary = ereMainWindow.CheckBoxControl(Name="My Library")
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

    # 初始化屏幕录制模块元素 Screen
    ScreenRecord = ereMainWindow.ButtonControl(foundIndex=10)
    ScreenShot = ereMainWindow.ButtonControl(foundIndex=11)





