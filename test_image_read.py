"""
测试图片读取功能（无GUI版本）
"""

import cv2
import numpy as np
import os

print("=" * 50)
print("测试图片读取功能")
print("=" * 50)

# 尝试多个可能的路径
img = None
possible_paths = [
    '../assets/sample-images/basic/landscape.jpg',  # 从src/examples/运行
    '../../assets/sample-images/basic/landscape.jpg',  # 从src/运行
    'assets/sample-images/basic/landscape.jpg',  # 从项目根目录运行
]

print(f"\n当前工作目录: {os.getcwd()}")
print("\n尝试读取图片...")

for i, path in enumerate(possible_paths, 1):
    print(f"  [{i}] 尝试: {path}")
    if os.path.exists(path):
        img = cv2.imread(path)
        if img is not None:
            print(f"      [OK] 成功! 图片尺寸: {img.shape}")
            break
    else:
        print(f"      [X] 文件不存在")

# 如果所有路径都失败，生成测试图片
if img is None:
    print("\n所有路径失败，生成测试图片...")
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    # 天空渐变
    for y in range(300):
        img[y, :] = [int(255 * y / 300), int(200 * y / 300), 100]
    # 草地
    img[300:, :] = [50, 150, 50]
    # 太阳
    cv2.circle(img, (500, 80), 50, (0, 255, 255), -1)
    print("✓ 测试图片生成成功!")

print(f"\n最终图片尺寸: {img.shape}")
print(f"数据类型: {img.dtype}")
print("\n测试完成!")
