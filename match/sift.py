import cv2
import numpy as np


def sift_feature_matching_with_box(template_image, target_image):
    # 1. 转换为灰度图
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    # 2. 创建SIFT对象
    sift = cv2.SIFT_create()

    # 3. 检测关键点和计算描述子
    keypoints_template, descriptors_template = sift.detectAndCompute(template_gray, None)
    keypoints_target, descriptors_target = sift.detectAndCompute(target_gray, None)

    # 4. 使用BFMatcher进行特征匹配，使用knnMatch找到k个最佳匹配
    bf = cv2.BFMatcher(cv2.NORM_L2)
    matches = bf.knnMatch(descriptors_target, descriptors_template, k=2)

    # 5. 过滤匹配结果，使用Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:  # Lowe's ratio test
            good_matches.append(m)

    # 6. 通过匹配计算单应性矩阵并找到目标图片在模板图片中的位置
    if len(good_matches) >= 4:  # 至少需要4个匹配点来计算单应性
        src_pts = np.float32([keypoints_target[m.queryIdx].pt for m in good_matches]).reshape(-1, 2)
        dst_pts = np.float32([keypoints_template[m.trainIdx].pt for m in good_matches]).reshape(-1, 2)

        # 计算单应性矩阵
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # 使用单应性矩阵变换目标图像的四个角点，找到在模板中的位置
        h, w = target_image.shape[:2]
        corners = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        transformed_corners = cv2.perspectiveTransform(corners, H)

        # 绘制目标位置框
        result_image = template_image.copy()
        result_image = cv2.polylines(result_image, [np.int32(transformed_corners)], True, (0, 255, 0), 3, cv2.LINE_AA)

        # 绘制所有匹配结果
        matches_img = cv2.drawMatches(target_image, keypoints_target, result_image, keypoints_template, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        return matches_img, transformed_corners, good_matches
    else:
        return None, None, None
