from configparser import ConfigParser

# 加载ere设置配置

# 修改配置文件
def modify_config(format, quality, frame_rate, frame_rate_mode, gpu_mode):
    """
    传入修改参数
    :param format:
    :param quality:
    :param frame_rate:
    :param frame_rate_mode:
    :param gpu_mode:
    :return:
    """
    config = ConfigParser()
    config.optionxform = str
    config.read(r"C:\Users\admini\AppData\Local\EaseUS\RecExperts\EreOptionsSettings.ini")
    # para_list = ["VideoFormat", "VideoQuality", "VideoFrameRate", "VideoRateMode", "RecordingEnableGPU"]


    # 修改ere设置配置文件
    if "VideoFormat" in config:
        config.set("VideoFormat", "currentIndex", format)
    else:
        config.add_section("VideoFormat")
        config.set("VideoFormat", "currentIndex", format)

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


modify_config("0", "0", "0", "0", "1")





