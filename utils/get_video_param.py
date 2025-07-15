import json
import os
import subprocess
import loguru


def get_latest_file_path(folder_path, file_extension):
    def traverse_directory(path):
        latest_package = None
        latest_package_date = None

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) and item.endswith(file_extension):
                file_date = os.path.getmtime(item_path)
                if latest_package_date is None or file_date > latest_package_date:
                    latest_package_date = file_date
                    latest_package = item_path

            elif os.path.isdir(item_path):
                # 递归调用遍历文件夹
                latest_package_subfolder = traverse_directory(item_path)
                if latest_package_subfolder:
                    file_date = os.path.getmtime(latest_package_subfolder)
                    if latest_package_date is None or file_date > latest_package_date:
                        latest_package_date = file_date
                        latest_package = latest_package_subfolder

        return latest_package
    # 调用遍历函数获取最新文件路径
    latest_package_path = traverse_directory(folder_path)
    if latest_package_path:
        return latest_package_path
    else:
        return None

def get_video_param(file_path):
    """
       使用 ffprobe 获取视频详细参数
       :param file_path: 视频文件路径
       :return: 包含视频参数的字典
       """
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        '-show_error',
        file_path
    ]
    loguru.logger.info(f"录制结果地址{file_path}")
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        # 输出原始结果用于调试
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode != 0:
            raise Exception(f"ffprobe 执行失败: {stderr}")

        if not stdout:
            raise Exception("ffprobe 未返回任何输出，请检查输入文件是否有效")

        video_info = json.loads(result.stdout)

        # 提取常用视频参数
        video_stream = None
        for stream in video_info.get('streams', []):
            if stream['codec_type'] == 'video':
                video_stream = stream
                break

        if not video_stream:
            raise Exception("未找到视频流")

        params = [
            "format:"+video_info.get('format', {}).get('format_name'),
            "duration:"+video_info.get('format', {}).get('duration', 0),  # 单位秒
            "bit_rate:"+str(int(video_info.get('format', {}).get('bit_rate', 0)) // 1024),  # 单位 kbps
            "width:"+str(video_stream.get('width')),
            "height:"+str(video_stream.get('height')),
            "fps:"+str(eval(video_stream.get('r_frame_rate'))),  # 如 "24000/1001" -> 23.98
            "codec:"+video_stream.get('codec_name'),
            "pixel_format:"+video_stream.get('pix_fmt'),
            "frame_count:"+str(video_stream.get('nb_frames', 0)),
            "rotate:"+str(video_stream.get('tags', {}).get('rotate'))
        ]

        return params

    except json.JSONDecodeError as e:
        raise Exception("ffprobe 返回结果解析失败", e)

if __name__ == '__main__':
    print(get_video_param(r"C:\Users\admini\Desktop\坤.mp4"))