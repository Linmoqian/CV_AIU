"""
OpenCV基础示例：图像的读取、显示和保存

学习目标:
    1. 掌握cv2.imread()读取图片
    2. 掌握cv2.imshow()显示图片
    3. 掌握cv2.imwrite()保存图片
    4. 了解中文路径的处理方法
"""

import cv2
import numpy as np
import sys
import os

# 添加utils目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from io_helpers import imread_chinese, imwrite_chinese, get_image_path

# ==================== 1. 读取图像 ====================
print("=" * 50)
print("1. 读取图像")
print("=" * 50)

# 读取彩色图（默认）
# 智能查找图片路径
img_path = get_image_path('sample-images/basic/landscape.jpg')
if img_path is None:
    print("错误：无法找到图片文件！")
    print("请运行 'assets/生成测试图片.py' 生成测试图片")
    exit()

img = imread_chinese(img_path)
print(f"[OK] 图片读取成功: {os.path.basename(img_path)}")
print(f"    完整路径: {img_path}")

# 读取灰度图（方法1：直接读取）
img_gray = imread_chinese(img_path, cv2.IMREAD_GRAYSCALE)

# 读取灰度图（方法2：从彩色图转换）
img_gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ==================== 2. 查看图像属性 ====================
print("\n" + "=" * 50)
print("2. 图像属性")
print("=" * 50)

print(f"图像形状: {img.shape}")
print(f"  - 高度: {img.shape[0]} 像素")
print(f"  - 宽度: {img.shape[1]} 像素")
print(f"  - 通道数: {img.shape[2]}")

print(f"\n图像尺寸: {img.size} 像素")
print(f"数据类型: {img.dtype}")

# ==================== 3. 访问像素 ====================
print("\n" + "=" * 50)
print("3. 像素访问")
print("=" * 50)

# 访问单个像素（返回BGR值）
pixel = img[100, 100]
print(f"像素(100, 100)的BGR值: {pixel}")

# 访问单个通道
blue = img[100, 100, 0]
green = img[100, 100, 1]
red = img[100, 100, 2]
print(f"  B={blue}, G={green}, R={red}")

# ==================== 4. 显示图像 ====================
print("\n" + "=" * 50)
print("4. 显示图像")
print("=" * 50)

# 显示彩色图
cv2.imshow('Color Image', img)

# 显示灰度图
cv2.imshow('Grayscale Image', img_gray)

# 等待按键（0表示无限等待）
print("按任意键关闭窗口...")
cv2.waitKey(0)

# 关闭所有窗口
cv2.destroyAllWindows()

# ==================== 5. 保存图像 ====================
print("\n" + "=" * 50)
print("5. 保存图像")
print("=" * 50)

# 保存灰度图
cv2.imwrite('output_gray.jpg', img_gray)
print("[OK] 灰度图已保存为: output_gray.jpg")

# 保存为PNG格式（无损）
cv2.imwrite('output_gray.png', img_gray)
print("[OK] 灰度图已保存为: output_gray.png")

# ==================== 6. 创建测试图像 ====================
print("\n" + "=" * 50)
print("6. 创建测试图像")
print("=" * 50)

# 创建一个300x300的蓝色图像
test_img = np.zeros((300, 300, 3), dtype=np.uint8)
test_img[:] = (255, 0, 0)  # BGR格式：蓝色

# 添加文字
cv2.putText(test_img, 'OpenCV Test', (50, 150),
           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

# 保存测试图像
cv2.imwrite('test_image.jpg', test_img)
print("[OK] 测试图像已保存为: test_image.jpg")

# 显示测试图像
cv2.imshow('Test Image', test_img)
cv2.waitKey(2000)  # 显示2秒后自动关闭
cv2.destroyAllWindows()

print("\n程序运行完成！")
