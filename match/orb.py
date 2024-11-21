# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : orb.py
# Time       ：2024/11/21 14:04
# Author     ：author name
# version    ：python 3.8
# Description：
"""
import cv2
import numpy as np
from ImageBase.Size import Point, Rect

from ImageBase import utils


def create_detector(**kwargs):  # 初始化检查器
    nfeatures = kwargs.get('nfeatures', 50000)
    scaleFactor = kwargs.get('scaleFactor', 1.2)
    nlevels = kwargs.get('nlevels', 8)
    edgeThreshold = kwargs.get('edgeThreshold', 31)
    firstLevel = kwargs.get('firstLevel', 0)
    WTA_K = kwargs.get('WTA_K', 2)
    scoreType = kwargs.get('scoreType', cv2.ORB_HARRIS_SCORE)
    patchSize = kwargs.get('patchSize', 31)
    fastThreshold = kwargs.get('fastThreshold', 20)

    params = dict(
        nfeatures=nfeatures, scaleFactor=scaleFactor, nlevels=nlevels,
        edgeThreshold=edgeThreshold, firstLevel=firstLevel, WTA_K=WTA_K,
        scoreType=scoreType, patchSize=patchSize, fastThreshold=fastThreshold,
    )
    detector = cv2.ORB_create(**params)
    return detector


def create_descriptor():
    # https://docs.opencv.org/master/d7/d99/classcv_1_1xfeatures2d_1_1BEBLID.html
    # https://github.com/iago-suarez/beblid-opencv-demo
    descriptor = cv2.xfeatures2d.BEBLID_create(0.75)
    return descriptor


def get_keypoint_and_descriptor(image):
    keypoints = create_detector().detect(image)
    # print(keypoints)
    keypoints, descriptors = create_descriptor().compute(image, keypoints)
    if len(keypoints) < 2:
        raise WindowsError('detect not enough feature points in input images')
    return keypoints, descriptors


def match_descriptor(image_template, image2):
    kp_src, des_src = get_keypoint_and_descriptor(image_template)
    kp_dst, des_dst = get_keypoint_and_descriptor(image2)
    bf = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = bf.knnMatch(des_src, des_dst, k=2)
    # matches = sorted(matches, key=lambda x: x.distance)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    if len(matches) > 4:  # 至少需要 4 个点来计算单应性
        # 获取匹配点的坐标
        template_pts = np.float32([kp_src[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        target_pts = np.float32([kp_dst[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算单应性矩阵
        H, mask = cv2.findHomography(template_pts, target_pts, cv2.RANSAC, 5.0)

        # 使用单应性矩阵计算模板图像在目标图像中的位置
        print(image_template.size)
        h, w = image_template.shape[:2]  # 模板图片尺寸
        corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)  # 模板的四个角点
        transformed_corners = cv2.perspectiveTransform(corners, H)  # 映射到目标图像的位置

        # 计算中心点
        center_x = int(np.mean(transformed_corners[:, 0, 0]))
        center_y = int(np.mean(transformed_corners[:, 0, 1]))
        point = Point(center_x, center_y)

    # 绘制匹配结果
    result = cv2.drawMatches(image_template, kp_src, image2, kp_dst, good_matches, None,
                             flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # 显示结果
    cv2.imshow('Matches', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return point


if __name__ == '__main__':
    image1 = utils.read_images(r'../test/screen.png')
    cv2.imshow('image_template', image1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    get_keypoint_and_descriptor(image1)
