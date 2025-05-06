import uiautomation as auto

class EreRecordingWindow:
    # 初始化录制过程中的录制条按钮元素
    RecordingBar = auto.WindowControl(Name="EaseUSExcludeWnd")
    Pause = RecordingBar.ButtonControl(foundIndex=1)
    Stop = RecordingBar.ButtonControl(foundIndex=2)
    Stop.MoveCursorToMyCenter()