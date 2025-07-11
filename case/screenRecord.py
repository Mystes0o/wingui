import os
import subprocess
import time
from utils.monitoring import Monitoring, WindowsManagerMonitoring
from utils.ini_op import modify_config, modify_save_config
from utils.excel_op import excel_to_list2
from utils.get_video_param import get_video_param, get_latest_file_path
from match.EreMainWindow import EreMainWindow
from match.EreMainWindow import ScreenRecordWindow, AudioRecordWindow
from match.EreMainWindow import ErePlayerWindow
from match.EreMainWindow import send_key, get_screen_size, drag
import loguru


monitor = Monitoring()
monitor_taskmgr = WindowsManagerMonitoring()
current_script_path = os.path.abspath(__file__)
project_path = os.path.dirname(current_script_path)

def full_screen_record():
    """
    :return: none
    """
    #录制结果初始化、录制文件位置
    record_result = []
    record_time = time.strftime("%Y_%m_%d_%H%M%S")
    record_save_path = os.path.join(project_path, record_time)
    os.makedirs(record_save_path, exist_ok=True)

    #录制参数修改
    record_param = excel_to_list2(r"C:\Users\admini\Desktop\ERE性能测试用例_模板.xlsx")
    for i in record_param:
        modify_config(i[0], i[1], i[2], i[3], i[4])
        record_save_path_ini = record_save_path.replace('\\', '/')
        modify_save_config(record_save_path_ini)
        time.sleep(3)


        # 主界面流程
        ere_main_window = EreMainWindow()
        ere_main_window.StartRecording.Click()
        ere_main_window.FullScreen.Click()

        # 记录信息
        screen_record_window = ScreenRecordWindow()
        screen_record_window_button = screen_record_window.ScreenRecord
        if screen_record_window_button.Exists(maxSearchSeconds=5):
            screen_record_window_button.Click()
        else:
            loguru.logger.error('未找到录制按钮')
            return 0
        # loguru.logger.info('录制' + str(i[5]) +'秒')
        loguru.logger.info('录制' + str(10) + '秒')
        start = monitor_taskmgr.monitoring_start()
        time.sleep(10+4)
        send_key('{F9}')

        # 初始结果
        result_source = monitor_taskmgr.monitoring_stop(start)
        result_video = get_latest_file_path(record_save_path, '.mp4')
        result_info = get_video_param(result_video)
        result_list = [result_source, result_info, result_video]
        record_result.append(result_list)
        print(record_result)

        # 录制结束
        time.sleep(2)
        ere_player_window = ErePlayerWindow()
        ere_player_window.Close.Click()



def custom_record(record_time):


    # 主界面流程
    ere_main_window = EreMainWindow()
    ere_main_window.StartRecording.Click()
    ere_main_window.Custom.Click()

    # 选择录制区域
    screen_size = get_screen_size()
    time.sleep(0.5)
    drag(1, 1, screen_size[0]-10, screen_size[1]-10)

    # 记录信息
    screen_record_window = ScreenRecordWindow()
    screen_record_window_button = screen_record_window.ScreenRecord
    if screen_record_window_button.Exists(maxSearchSeconds=5):
        screen_record_window_button.Click()
    else:
        loguru.logger.info('未找到录制按钮')
        return 0
    loguru.logger.info('录制' + str(record_time) + '秒')
    start = monitor.monitoring_start()
    time.sleep(record_time + 4)
    send_key('{F9}')
    monitor.monitoring_stop(start)

    # 录制结束
    time.sleep(2)
    erePlayerWindow = ErePlayerWindow()
    erePlayerWindow.Close.Click()

def window_record(record_time):
    pass

def audio_record(record_time):
    # 主界面流程
    ere_main_window = EreMainWindow()
    ere_main_window.StartRecording.Click()
    ere_main_window.Audio.Click()

    # 记录信息
    audio_record_window = AudioRecordWindow()
    audio_record_window_button = audio_record_window.AudioRecord
    if audio_record_window_button.Exists(maxSearchSeconds=5):
        audio_record_window_button.Click()
    else:
        loguru.logger.info('未找到录制按钮')
        return 0
    loguru.logger.info('录制' + str(record_time) + '秒')
    start = monitor.monitoring_start()
    time.sleep(record_time + 4)
    send_key('{F9}')
    monitor.monitoring_stop(start)

    # 录制结束
    time.sleep(2)
    ere_player_window = ErePlayerWindow()
    ere_player_window.Close.Click()




def switch(times):
    for i in range(times):
        EreMainWindow.MyLibrary.Click()
        EreMainWindow.StartRecording.Click()



if __name__ == '__main__':
    full_screen_record()
    # switch(100)