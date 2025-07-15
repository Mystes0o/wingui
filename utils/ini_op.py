import time
from configparser import ConfigParser
import loguru


# 加载ere设置配置

# 修改配置文件

def modify_save_config(save_path):
    save_path = str(save_path)
    config = ConfigParser()
    config.optionxform = str
    config.read(r"C:\Users\admini\AppData\Local\EaseUS\RecExperts\EreSettings.ini")
    # 修改录制保存地址
    if "Record" in config:
        config.set("Record", "outputDir", save_path)
    else:
        config.add_section("Record")
        config.set("Record", "outputDir", save_path)

    # 保存
    with open(r"C:\Users\admini\AppData\Local\EaseUS\RecExperts\EreSettings.ini", 'w') as f:
        config.write(f)
def modify_config(formate, quality, frame_rate, frame_rate_mode, gpu_mode):
    """
    传入修改参数
    :param save_path:
    :param formate:
    :param quality:
    :param frame_rate:
    :param frame_rate_mode:
    :param gpu_mode:
    :return:
    """
    formate = str(formate)
    quality = str(quality)
    frame_rate = str(frame_rate)
    frame_rate_mode = str(frame_rate_mode)
    gpu_mode = str(gpu_mode)
    config = ConfigParser()
    config.optionxform = str
    config.read(r"C:\Users\admini\AppData\Local\EaseUS\RecExperts\EreOptionsSettings.ini")
    # para_list = ["VideoFormat", "VideoQuality", "VideoFrameRate", "VideoRateMode", "RecordingEnableGPU"]


    # 修改ere设置配置文件
    if "VideoFormat" in config:
        config.set("VideoFormat", "currentIndex", formate)
    else:
        config.add_section("VideoFormat")
        config.set("VideoFormat", "currentIndex", formate)

    if "VideoQuality" in config:
        config.set("VideoQuality", "currentIndex", quality)
    else:
        config.add_section("VideoQuality")
        config.set("VideoQuality", "currentIndex", quality)

    if "VideoFrameRate" in config:
        config.set("VideoFrameRate", "currentIndex", frame_rate)
    else:
        config.add_section("VideoFrameRate")
        config.set("VideoFrameRate", "currentIndex", frame_rate)

    if "VideoRateMode" in config:
        config.set("VideoRateMode", "currentIndex", frame_rate_mode)
    else:
        config.add_section("VideoRateMode")
        config.set("VideoRateMode", "currentIndex", frame_rate_mode)

    if "RecordingEnableGPU" in config:
        config.set("RecordingEnableGPU", "currentIndex", gpu_mode)
    else:
        config.add_section("RecordingEnableGPU")
        config.set("RecordingEnableGPU", "currentIndex", gpu_mode)

    #保存
    with open(r"C:\Users\admini\AppData\Local\EaseUS\RecExperts\EreOptionsSettings.ini", 'w') as f:
        config.write(f)

    loguru.logger.info(f"修改ere设置配置文件成功:{formate} {quality} {frame_rate} {frame_rate_mode} {gpu_mode}")

if __name__ == '__main__':
    modify_save_config(r'E:\python\wingui\case\2025_07_11_101550')





