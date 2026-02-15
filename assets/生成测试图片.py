"""
自动生成OpenCV培训所需的测试图片

运行此脚本将在assets/sample-images/目录下生成各种测试图片
"""

import cv2
import numpy as np
import os
import sys

# 创建输出目录（处理相对路径问题）
if os.path.basename(os.getcwd()) == 'assets':
    # 如果在assets目录下运行
    output_dir = './sample-images'
else:
    # 否则使用原路径
    output_dir = './assets/sample-images'

subdirs = ['basic', 'colored-objects', 'noisy', 'shapes', 'real-world']

for subdir in subdirs:
    os.makedirs(f'{output_dir}/{subdir}', exist_ok=True)

print("=" * 60)
print("OpenCV培训测试图片生成器")
print("=" * 60)

# ==================== 1. 基础图片 ====================
print("\n1. 生成基础图片...")

# 创建风景图（渐变色）
landscape = np.zeros((400, 600, 3), dtype=np.uint8)
# 天空渐变
for y in range(300):
    landscape[y, :] = [int(255 * y / 300), int(200 * y / 300), 100]
# 草地
landscape[300:, :] = [50, 150, 50]
# 太阳
cv2.circle(landscape, (500, 80), 50, (0, 255, 255), -1)
cv2.imwrite(f'{output_dir}/basic/landscape.jpg', landscape)
print("  [OK] landscape.jpg - 风景图")

# 创建人像图（简单的人脸）
portrait = np.zeros((400, 300, 3), dtype=np.uint8)
portrait[:] = (200, 180, 150)  # 肤色背景
# 脸部轮廓
cv2.ellipse(portrait, (150, 200), (100, 130), 0, 0, 360, (180, 160, 130), -1)
# 眼睛
cv2.circle(portrait, (110, 170), 15, (0, 0, 0), -1)
cv2.circle(portrait, (190, 170), 15, (0, 0, 0), -1)
# 鼻子
cv2.circle(portrait, (150, 210), 10, (150, 130, 110), -1)
# 嘴巴
cv2.ellipse(portrait, (150, 250), (30, 15), 0, 0, 180, (0, 0, 150), 2)
cv2.imwrite(f'{output_dir}/basic/portrait.jpg', portrait)
print("  [OK] portrait.jpg - 人像图")

# 创建文字图
text_img = np.zeros((300, 600, 3), dtype=np.uint8)
text_img[:] = (255, 255, 255)
cv2.putText(text_img, 'OpenCV Training', (50, 100),
           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
cv2.putText(text_img, 'Computer Vision', (50, 180),
           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
cv2.putText(text_img, 'Image Processing', (50, 250),
           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
cv2.imwrite(f'{output_dir}/basic/text.jpg', text_img)
print("  [OK] text.jpg - 文字图")

# ==================== 2. 彩色物体 ====================
print("\n2. 生成彩色物体图片...")

# 红苹果
apple = np.zeros((400, 400, 3), dtype=np.uint8)
apple[:] = (240, 240, 240)  # 浅灰背景
cv2.circle(apple, (200, 200), 100, (0, 0, 255), -1)  # 红色圆形
# 叶子
cv2.ellipse(apple, (200, 110), (30, 15), 45, 0, 360, (0, 255, 0), -1)
cv2.imwrite(f'{output_dir}/colored-objects/red-apple.jpg', apple)
print("  [OK] red-apple.jpg - 红苹果")

# 蓝球
blue_ball = np.zeros((400, 400, 3), dtype=np.uint8)
blue_ball[:] = (240, 240, 240)
cv2.circle(blue_ball, (200, 200), 100, (255, 0, 0), -1)  # 蓝色圆形
# 球的纹理
for i in range(5):
    cv2.line(blue_ball, (100+i*40, 150), (100+i*40, 250), (200, 0, 0), 2)
cv2.imwrite(f'{output_dir}/colored-objects/blue-ball.jpg', blue_ball)
print("  [OK] blue-ball.jpg - 蓝球")

# 混合颜色
mixed = np.zeros((400, 600, 3), dtype=np.uint8)
mixed[:] = (240, 240, 240)
cv2.circle(mixed, (100, 200), 60, (0, 0, 255), -1)  # 红
cv2.circle(mixed, (250, 200), 60, (0, 255, 0), -1)  # 绿
cv2.circle(mixed, (400, 200), 60, (255, 0, 0), -1)  # 蓝
cv2.rectangle(mixed, (50, 320), (140, 380), (0, 255, 255), -1)  # 黄
cv2.imwrite(f'{output_dir}/colored-objects/mixed-colors.jpg', mixed)
print("  [OK] mixed-colors.jpg - 混合颜色")

# ==================== 3. 含噪图片 ====================
print("\n3. 生成含噪图片...")

# 高斯噪声
clean = np.zeros((300, 400, 3), dtype=np.uint8)
cv2.rectangle(clean, (50, 50), (350, 250), (128, 128, 128), -1)
cv2.putText(clean, 'Clean', (120, 160),
           cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

gaussian_noise = clean.copy()
noise = np.random.normal(0, 30, clean.shape).astype(np.uint8)
gaussian_noise = cv2.add(gaussian_noise, noise)
cv2.imwrite(f'{output_dir}/noisy/noisy-gaussian.jpg', gaussian_noise)
print("  [OK] noisy-gaussian.jpg - 高斯噪声")

# 椒盐噪声
salt_pepper = clean.copy()
# 添加盐噪声（白点）
num_salt = int(0.05 * clean.size * clean.shape[2])
coords = [np.random.randint(0, i, num_salt) for i in clean.shape]
salt_pepper[coords[0], coords[1], coords[2]] = 255
# 添加椒噪声（黑点）
num_pepper = int(0.05 * clean.size * clean.shape[2])
coords = [np.random.randint(0, i, num_pepper) for i in clean.shape]
salt_pepper[coords[0], coords[1], coords[2]] = 0

cv2.imwrite(f'{output_dir}/noisy/noisy-salt-pepper.jpg', salt_pepper)
print("  [OK] noisy-salt-pepper.jpg - 椒盐噪声")

# 干净参考图
cv2.imwrite(f'{output_dir}/noisy/clean-reference.jpg', clean)
print("  [OK] clean-reference.jpg - 干净参考图")

# ==================== 4. 几何形状 ====================
print("\n4. 生成几何形状图片...")

# 硬币
coins = np.zeros((400, 600, 3), dtype=np.uint8)
coins[:] = (200, 200, 200)
coin_positions = [(150, 200), (300, 200), (450, 200), (225, 280), (375, 280)]
for pos in coin_positions:
    cv2.circle(coins, pos, 50, (100, 100, 150), -1)  # 银色
    cv2.circle(coins, pos, 40, (120, 120, 170), 2)  # 内圈
cv2.imwrite(f'{output_dir}/shapes/coins.jpg', coins)
print("  [OK] coins.jpg - 硬币")

# 圆形
circles = np.zeros((400, 600, 3), dtype=np.uint8)
circles[:] = (240, 240, 240)
cv2.circle(circles, (150, 200), 80, (255, 0, 0), -1)
cv2.circle(circles, (300, 200), 60, (0, 255, 0), -1)
cv2.circle(circles, (450, 200), 100, (0, 0, 255), -1)
cv2.circle(circles, (225, 320), 50, (255, 255, 0), -1)
cv2.circle(circles, (375, 320), 70, (255, 0, 255), -1)
cv2.imwrite(f'{output_dir}/shapes/circles.png', circles)
print("  [OK] circles.png - 圆形")

# 矩形
rectangles = np.zeros((400, 600, 3), dtype=np.uint8)
rectangles[:] = (240, 240, 240)
cv2.rectangle(rectangles, (50, 50), (200, 200), (255, 0, 0), -1)
cv2.rectangle(rectangles, (250, 50), (400, 200), (0, 255, 0), -1)
cv2.rectangle(rectangles, (450, 50), (550, 200), (0, 0, 255), -1)
cv2.rectangle(rectangles, (100, 250), (250, 350), (255, 255, 0), -1)
cv2.rectangle(rectangles, (300, 250), (500, 350), (255, 0, 255), -1)
cv2.imwrite(f'{output_dir}/shapes/rectangles.png', rectangles)
print("  [OK] rectangles.png - 矩形")

# ==================== 5. 真实场景模拟 ====================
print("\n5. 生成真实场景模拟图片...")

# 文档
document = np.zeros((600, 800, 3), dtype=np.uint8)
document[:] = (255, 255, 255)
# 模拟文字行
for i in range(10):
    y = 80 + i * 50
    cv2.rectangle(document, (100, y), (700, y + 30), (0, 0, 0), -1)
# 标题
cv2.rectangle(document, (100, 30), (700, 60), (0, 0, 150), -1)
cv2.imwrite(f'{output_dir}/real-world/document.jpg', document)
print("  [OK] document.jpg - 文档")

# 车牌模拟
license_plate = np.zeros((200, 400, 3), dtype=np.uint8)
license_plate[:] = (255, 255, 255)
cv2.rectangle(license_plate, (20, 50), (380, 150), (0, 0, 200), -1)
# 蓝色区域
cv2.rectangle(license_plate, (30, 60), (120, 140), (255, 255, 255), -1)
# 字符模拟
cv2.putText(license_plate, 'A', (40, 120),
           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
cv2.putText(license_plate, '12345', (140, 120),
           cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
cv2.imwrite(f'{output_dir}/real-world/license-plate.jpg', license_plate)
print("  [OK] license-plate.jpg - 车牌")

# 人脸模拟
face = np.zeros((400, 400, 3), dtype=np.uint8)
face[:] = (200, 200, 200)
cv2.ellipse(face, (200, 200), (150, 200), 0, 0, 360, (180, 160, 140), -1)
# 眼睛
cv2.ellipse(face, (130, 160), (30, 20), 0, 0, 360, (255, 255, 255), -1)
cv2.ellipse(face, (270, 160), (30, 20), 0, 0, 360, (255, 255, 255), -1)
cv2.circle(face, (130, 160), 10, (0, 0, 0), -1)
cv2.circle(face, (270, 160), 10, (0, 0, 0), -1)
# 眉毛
cv2.line(face, (100, 130), (160, 130), (50, 30, 10), 5)
cv2.line(face, (240, 130), (300, 130), (50, 30, 10), 5)
# 鼻子
pts = np.array([[200, 180], [180, 240], [220, 240]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.fillPoly(face, [pts], (150, 130, 110))
# 嘴巴
cv2.ellipse(face, (200, 290), (50, 25), 0, 0, 180, (100, 50, 50), 3)
cv2.imwrite(f'{output_dir}/real-world/face.jpg', face)
print("  [OK] face.jpg - 人脸")

print("\n" + "=" * 60)
print("所有测试图片生成完成！")
print(f"图片保存在: {output_dir}/")
print("=" * 60)

# 生成图片清单
print("\n生成的图片清单:")
for subdir in subdirs:
    files = os.listdir(f'{output_dir}/{subdir}')
    print(f"\n{subdir}/ ({len(files)} 张):")
    for file in files:
        print(f"  - {file}")
