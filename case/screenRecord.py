import time
import pyautogui
from WinGuiBase import Win
from utils.monitoring import Monitoring
from match.EreMainWindow import EreMainWindow


def record_monitor(record_time):
    EreMain = Win(handle_title='EaseUs RecExperts')
    EreMain.click_text('Screen')
    time.sleep(2)
    EreMainWindow.ScreenRecord.Click()
    monitoring = Monitoring()
    a = monitoring.monitoring_start()
    time.sleep(record_time)
    monitoring.monitoring_stop(a)
    pyautogui.hotkey('f9')

if __name__ == '__main__':
    record_monitor(record_time=120)
