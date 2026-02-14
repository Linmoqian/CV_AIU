"""
OpenCV示例：图像滤波与增强

学习目标:
    1. 掌握均值滤波、高斯滤波、中值滤波
    2. 理解双边滤波的效果
    3. 学会图像锐化
    4. 掌握Canny边缘检测
"""

import cv2
import numpy as np

print("图像滤波与边缘检测")

# 读取含噪图片
img = cv2.imread('../assets/sample-images/noisy/noisy-gaussian.jpg')

if img is None:
    print("警告：无法读取含噪图片，生成测试图片...")
    # 生成测试图片
    clean = np.zeros((300, 400, 3), dtype=np.uint8)
    cv2.rectangle(clean, (50, 50), (350, 250), (128, 128, 128), -1)
    cv2.putText(clean, 'Test Image', (100, 160),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    # 添加噪声
    noise = np.random.normal(0, 30, clean.shape).astype(np.uint8)
    img = cv2.add(clean, noise)

# ==================== 1. 图像平滑 ====================
print("\n1. 图像平滑（去噪）")

# 均值滤波
blur_mean = cv2.blur(img, (5, 5))
print("  [OK] 均值滤波 (5x5)")

# 高斯滤波
blur_gaussian = cv2.GaussianBlur(img, (5, 5), 0)
print("  [OK] 高斯滤波 (5x5)")

# 中值滤波
blur_median = cv2.medianBlur(img, 5)
print("  [OK] 中值滤波 (5x5)")

# 双边滤波（美颜效果）
blur_bilateral = cv2.bilateralFilter(img, 15, 80, 80)
print("  [OK] 双边滤波")

# ==================== 2. 对比显示 ====================
print("\n2. 对比显示滤波效果")

# 创建对比图
row1 = np.hstack([img,
                  blur_mean,
                  blur_gaussian])
row2 = np.hstack([blur_median,
                  blur_bilateral])

result = np.vstack([row1, row2])
result = cv2.resize(result, None, fx=0.6, fy=0.6)

cv2.imshow('Filtering Comparison', result)
print("按任意键继续...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# ==================== 3. 图像锐化 ====================
print("\n3. 图像锐化")

# 读取模糊图片（或使用原图）
blur_img = cv2.GaussianBlur(img, (15, 15), 0)

# 定义锐化核
kernel_sharpen = np.array([
    [-1, -1, -1],
    [-1,  9, -1],
    [-1, -1, -1]
])

# 应用锐化
sharpened = cv2.filter2D(blur_img, -1, kernel_sharpen)
print("  [OK] 锐化处理")

# 拉普拉斯锐化
laplacian = cv2.Laplacian(blur_img, cv2.CV_64F)
laplacian = np.uint8(np.absolute(laplacian))
sharpened_lap = cv2.add(blur_img, laplacian)
print("  [OK] 拉普拉斯锐化")

# 显示对比
row = np.hstack([blur_img, sharpened, sharpened_lap])
row = cv2.resize(row, None, fx=0.6, fy=0.6)
cv2.imshow('Sharpening Comparison', row)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ==================== 4. 边缘检测 ====================
print("\n4. 边缘检测")

# 转灰度
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Sobel边缘检测
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobelx = np.uint8(np.absolute(sobelx))

sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobely = np.uint8(np.absolute(sobely))

sobel_combined = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)

print("  [OK] Sobel边缘检测")

# Canny边缘检测
edges = cv2.Canny(gray, 50, 150)
print("  [OK] Canny边缘检测 (50, 150)")

# 自动阈值Canny
median = np.median(gray)
lower = int(max(0, 0.7 * median))
upper = int(min(255, 1.3 * median))
edges_auto = cv2.Canny(gray, lower, upper)
print(f"  [OK] Canny自动阈值 ({lower}, {upper})")

# 显示边缘检测结果
row1 = np.hstack([cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(sobelx, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(sobely, cv2.COLOR_GRAY2BGR)])
row2 = np.hstack([cv2.cvtColor(sobel_combined, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(edges_auto, cv2.COLOR_GRAY2BGR)])

result = np.vstack([row1, row2])
result = cv2.resize(result, None, fx=0.5, fy=0.5)

cv2.imshow('Edge Detection', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ==================== 5. 保存结果 ====================
print("\n5. 保存结果 (已禁用)")

# 保存功能已禁用，如需保存请取消以下注释
# cv2.imwrite('filtering_gaussian.jpg', blur_gaussian)
# cv2.imwrite('filtering_bilateral.jpg', blur_bilateral)
# cv2.imwrite('edges_canny.jpg', edges)
# cv2.imwrite('edges_auto.jpg', edges_auto)
print("  [提示] 图片保存功能已禁用，避免生成多余文件")

print("\n程序运行完成！")
