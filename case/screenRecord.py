import os
import subprocess
import time
import pythoncom
import psutil
import uiautomation as auto

from utils.monitoring import Monitoring, WindowsManagerMonitoring
from utils.ini_op import modify_config, modify_save_config
from utils.excel_op import excel_to_list2, list_to_excel
from utils.get_video_param import get_video_param, get_latest_file_path
from match.EreMainWindow import send_key, get_screen_size, drag
import loguru


monitor = Monitoring()
monitor_taskmgr = WindowsManagerMonitoring()
current_script_path = os.path.abspath(__file__)
project_path = os.path.dirname(current_script_path)


def full_screen_record(formate, quality, frame_rate, frame_rate_mode, gpu_mode, video_len):
    """
    :return: none
    """

    #录制参数修改
    modify_config(formate, quality, frame_rate, frame_rate_mode, gpu_mode)
    subprocess.Popen([r"C:\Program Files (x86)\EaseUS\RecExperts\bin\RecExperts.exe"])
    time.sleep(5)

    # 主界面流程
    ere_main_window =  auto.WindowControl(Name="EaseUS RecExperts", searchFromControl=auto.GetRootControl(), foundIndex=1)
    ere_main_window.ButtonControl(Name="MainScreenFunButton").Click()
    ere_main_window.CheckBoxControl(Name="Start Recording")

    screen_record_window = auto.WindowControl(Name="EaseUS RecExperts", searchFromControl=auto.GetRootControl(), foundIndex=1)
    screen_record_window_button = screen_record_window.ButtonControl(foundIndex=11)
    if screen_record_window_button.Exists(maxSearchSeconds=5):
        screen_record_window_button.Click()
    else:
        loguru.logger.error('未找到录制按钮')
        return 0

    # 记录信息
    loguru.logger.info('录制' + str(video_len) +'秒')
    start = monitor_taskmgr.monitoring_start()
    time.sleep(video_len+4)
    send_key('{F9}')
    result_source = monitor_taskmgr.monitoring_stop(start)
    time.sleep(1)

    # 录制结束，关闭ere
    os.system("taskkill /f /im RecExperts.exe")

    return result_source



# def custom_record(record_time):
#
#
#     # 主界面流程
#     ere_main_window = EreMainWindow()
#     ere_main_window.StartRecording.Click()
#     ere_main_window.Custom.Click()
#
#     # 选择录制区域
#     screen_size = get_screen_size()
#     time.sleep(0.5)
#     drag(1, 1, screen_size[0]-10, screen_size[1]-10)
#
#     # 记录信息
#     screen_record_window = ScreenRecordWindow()
#     screen_record_window_button = screen_record_window.ScreenRecord
#     if screen_record_window_button.Exists(maxSearchSeconds=5):
#         screen_record_window_button.Click()
#     else:
#         loguru.logger.info('未找到录制按钮')
#         return 0
#     loguru.logger.info('录制' + str(record_time) + '秒')
#     start = monitor.monitoring_start()
#     time.sleep(record_time + 4)
#     send_key('{F9}')
#     monitor.monitoring_stop(start)
#
#     # 录制结束
#     time.sleep(2)
#     erePlayerWindow = ErePlayerWindow()
#     erePlayerWindow.Close.Click()

# def window_record(record_time):
#     pass

# def audio_record(record_time):
#     # 主界面流程
#     ere_main_window = EreMainWindow()
#     ere_main_window.StartRecording.Click()
#     ere_main_window.Audio.Click()
#
#     # 记录信息
#     audio_record_window = AudioRecordWindow()
#     audio_record_window_button = audio_record_window.AudioRecord
#     if audio_record_window_button.Exists(maxSearchSeconds=5):
#         audio_record_window_button.Click()
#     else:
#         loguru.logger.info('未找到录制按钮')
#         return 0
#     loguru.logger.info('录制' + str(record_time) + '秒')
#     start = monitor.monitoring_start()
#     time.sleep(record_time + 4)
#     send_key('{F9}')
#     monitor.monitoring_stop(start)
#
#     # 录制结束
#     time.sleep(2)
#     ere_player_window = ErePlayerWindow()
#     ere_player_window.Close.Click()




if __name__ == '__main__':

    # 录制结果初始化、录制文件位置
    record_time = time.strftime("%Y_%m_%d_%H%M%S")
    record_save_path = os.path.join(project_path, record_time)

    excel_path = os.path.join(project_path, 'ERE性能测试用例_模板.xlsx')
    record_param = excel_to_list2(excel_path)

    loguru.logger.info(f"文件保存地址:{record_save_path}")
    os.makedirs(record_save_path, exist_ok=True)
    record_save_path_ini = record_save_path.replace('\\', '/')
    modify_save_config(record_save_path_ini)

    result = []
    for i in record_param:
        time.sleep(3)
        result_list = full_screen_record(i[0], i[1], i[2], i[3], i[4], i[5])
        result_video = get_latest_file_path(record_save_path, '.mp4')
        result_info = get_video_param(result_video)
        result1 = [result_list, result_info, result_video]
        result.append(result1)

    list_to_excel(excel_path, result)


