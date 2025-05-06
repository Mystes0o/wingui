#  文本识别模块

import easyocr
import torch
from loguru import logger
from ImageBase.Size import Point
import cv2

# 初始化全局Reader（单例模式）
_reader = None


def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(
            ['en'],
            gpu=True,
            # model_storage_directory='./model',  # 指定模型缓存路径
            download_enabled=False  # 禁用自动下载
        )
    return _reader


def ocr_match(img, text, min_confidence=0.5, image_scale=None):
    """
    优化后的OCR匹配函数
    :param img: 输入图像(numpy数组或文件路径)
    :param text: 需要匹配的文本
    :param min_confidence: 最小置信度阈值(默认0.5)
    :param image_scale: 图像缩放比例(0-1)
    :return: (Point, confidence) 匹配结果
    """
    try:
        # 获取单例Reader
        reader = get_reader()

        # 图像预处理
        if isinstance(img, str):
            img = cv2.imread(img)

        if image_scale and 0 < image_scale < 1:
            h, w = img.shape[:2]
            img = cv2.resize(img, (int(w * image_scale), int(h * image_scale)))

        # 执行OCR识别（带性能优化参数）
        result = reader.readtext(
            img,
            batch_size=10,  # 适当增大批处理大小
            text_threshold=min_confidence,
            low_text=0.4,  # 过滤低质量文本
            link_threshold=0.4,  # 过滤孤立文字
            decoder='beamsearch',  # 平衡速度与精度
            beamWidth=5  # 适当减少搜索宽度
        )

        # 结果处理
        for item in result:
            bbox, detected_text, confidence = item
            if text == detected_text and confidence >= min_confidence:
                # 计算中心点坐标（考虑图像缩放）
                x_coords = [p[0] for p in bbox]
                y_coords = [p[1] for p in bbox]
                x = int((min(x_coords) + max(x_coords)) / 2)
                y = int((min(y_coords) + max(y_coords)) / 2)

                if image_scale:
                    x = int(x / image_scale)
                    y = int(y / image_scale)

                logger.debug(f"匹配成功: {text} @ ({x}, {y}), 置信度: {confidence:.2f}")
                return Point(x, y), confidence

        logger.debug(f"未找到匹配文本: {text}")
        return Point(0, 0), 0

    except Exception as e:
        logger.error(f"OCR处理失败: {str(e)}")
        # 清理GPU缓存
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return Point(0, 0), 0



if __name__ == '__main__':
    a = ocr_match(r'../test/audio.png', 'Audio')
    print(a)