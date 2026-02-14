#                    _ooOoo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                   O\  =  /O
#                ____/`---'\____
#              .'  \|     |//  `.
#             /  \|||  :  |||//             /  _||||| -:- |||||-             |   | \\  -  /// |   |
#            | \_|  ''\---/''  |   |
#            \  .-\__  `-`  ___/-. /
#          ___`. .'  /--.--\  `. . __
#       ."" '<  `.___\_<|>_/___.'  >'"".
#      | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#      \  \ `-.   \_ __\ /__ _/   .-` /  /
# ======`-.____`-.___\_____/___.-`____.-'======
#                    `=---='
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#             佛祖保佑       永无BUG

"""
OpenCV示例：图像基本操作

学习目标:
    1. 图像缩放
    2. 图像裁剪（ROI）
    3. 图像翻转
    4. 图像旋转
"""

import cv2
import numpy as np
import sys
import os

# 添加utils目录到路径（兼容中文路径和Jupyter）
if "__file__" in globals():
    utils_path = os.path.join(os.path.dirname(__file__), "..", "utils")
else:
    utils_path = os.path.abspath(os.path.join("..", "utils"))
if os.path.exists(utils_path):
    sys.path.append(utils_path)
    from io_helpers import imread_chinese, get_image_path

# 读取图像（使用中文路径兼容函数）
img_path = get_image_path('sample-images/basic/landscape.jpg')
if img_path is None:
    print("错误：无法找到图片文件！")
    exit()
img = imread_chinese(img_path)

if img is None:
    print("无法读取图片！")
    exit()

print("图像基本操作")

# ==================== 1. 图像缩放 ====================
print("\n1. 图像缩放")

height, width = img.shape[:2]
print(f"原始尺寸: {width} x {height}")

# 缩小50%
img_small = cv2.resize(img, None, fx=0.5, fy=0.5,
                      interpolation=cv2.INTER_AREA)
print(f"缩小50%: {img_small.shape[1]} x {img_small.shape[0]}")

# 放大2倍
img_large = cv2.resize(img, None, fx=2.0, fy=2.0,
                      interpolation=cv2.INTER_CUBIC)
print(f"放大2倍: {img_large.shape[1]} x {img_large.shape[0]}")

# 指定尺寸缩放（保持宽高比）
new_width = 800
scale = new_width / width
new_height = int(height * scale)
img_resized = cv2.resize(img, (new_width, new_height))
print(f"指定宽度800: {img_resized.shape[1]} x {img_resized.shape[0]}")

# ==================== 2. 图像裁剪 ====================
print("\n2. 图像裁剪")

# 裁剪中心区域
start_y, start_x = height // 4, width // 4
end_y, end_x = start_y * 3, start_x * 3

img_cropped = img[start_y:end_y, start_x:end_x]
print(f"裁剪区域: ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
print(f"裁剪后尺寸: {img_cropped.shape[1]} x {img_cropped.shape[0]}")

# ==================== 3. 图像翻转 ====================
print("\n3. 图像翻转")

# 水平翻转（镜像）
img_h_flip = cv2.flip(img, 1)

# 垂直翻转
img_v_flip = cv2.flip(img, 0)

# 同时水平和垂直翻转
img_hv_flip = cv2.flip(img, -1)

# ==================== 4. 图像旋转 ====================
print("\n4. 图像旋转")

# 围绕中心旋转45度
center = (width // 2, height // 2)
angle = 45
scale = 1.0

M = cv2.getRotationMatrix2D(center, angle, scale)
img_rotated = cv2.warpAffine(img, M, (width, height))

# 旋转90度（简单方法）
img_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# ==================== 5. 显示结果 ====================
print("\n显示结果...")
print("按任意键关闭所有窗口...")

# 创建大图显示所有结果
# 第一行：原图、缩小（调整到原尺寸）、放大（调整到原尺寸）
img_small_display = cv2.resize(img_small, (width, height))
img_large_display = cv2.resize(img_large, (width, height))
row1 = np.hstack([img, img_small_display, img_large_display])

# 第二行：裁剪（调整到原尺寸）、水平翻转、垂直翻转
img_cropped_display = cv2.resize(img_cropped, (width, height))
row2 = np.hstack([img_cropped_display, img_h_flip, img_v_flip])

# 第三行：旋转45度、旋转90度（调整到原尺寸）+ 黑色填充
img_90_display = cv2.resize(img_90, (width, height))
# 创建一个空白图像用于填充
blank = np.zeros_like(img)
row3 = np.hstack([img_rotated, img_90_display, blank])

# 垂直拼接所有行
result = np.vstack([row1, row2, row3])

# 调整显示大小
result_display = cv2.resize(result, None, fx=0.5, fy=0.5)

cv2.imshow('All Operations', result_display)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ==================== 6. 保存结果 ====================
print("\n保存结果 (已禁用)...")

# 保存功能已禁用，如需保存请取消以下注释
# cv2.imwrite('resized.jpg', img_resized)
# cv2.imwrite('cropped.jpg', img_cropped)
# cv2.imwrite('flipped_horizontal.jpg', img_h_flip)
# cv2.imwrite('rotated_45.jpg', img_rotated)
print("[提示] 图片保存功能已禁用，避免生成多余文件")

print("\n程序运行完成！")
