"""
OpenCV示例：图像阈值处理

学习目标:
    1. 掌握简单阈值处理
    2. 学会Otsu自动阈值
    3. 掌握自适应阈值
    4. 理解不同阈值方法的适用场景
"""

import cv2
import numpy as np

print("图像阈值处理")

# 读取图像
img = cv2.imread('../assets/sample-images/real-world/document.jpg')

if img is None:
    print("警告：无法读取文档图片，使用测试图片...")
    # 创建测试图片（模拟文档）
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    img[:] = (220, 220, 220)  # 浅灰背景
    # 添加文字行
    for i in range(8):
        y = 60 + i * 40
        cv2.rectangle(img, (80, y), (520, y + 25), (0, 0, 0), -1)
    # 标题
    cv2.rectangle(img, (80, 20), (520, 50), (0, 0, 150), -1)

# 转灰度
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ==================== 1. 简单阈值 ====================
print("\n1. 简单阈值处理")

# 固定阈值127
ret1, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
print(f"  [OK] BINARY 阈值=127")

# 反二值化
ret2, thresh2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
print(f"  [OK] BINARY_INV 阈值=127")

# 截断
ret3, thresh3 = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
print(f"  [OK] TRUNC 阈值=127")

# 低于阈值置0
ret4, thresh4 = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO)
print(f"  [OK] TOZERO 阈值=127")

# ==================== 2. Otsu阈值 ====================
print("\n2. Otsu自动阈值")

# 全局手动阈值
ret_manual, thresh_manual = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
print(f"  手动阈值: {ret_manual}")

# Otsu自动阈值
ret_otsu, thresh_otsu = cv2.threshold(gray, 0, 255,
                                      cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(f"  [OK] Otsu阈值: {ret_otsu}")

# ==================== 3. 自适应阈值 ====================
print("\n3. 自适应阈值")

# 自适应均值阈值
thresh_mean = cv2.adaptiveThreshold(gray, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
print("  [OK] 自适应均值阈值 (11, 2)")

# 自适应高斯阈值
thresh_gaussian = cv2.adaptiveThreshold(gray, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
print("  [OK] 自适应高斯阈值 (11, 2)")

# ==================== 4. 对比显示 ====================
print("\n4. 对比显示")

# 简单阈值对比
row1 = np.hstack([cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(thresh1, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(thresh_otsu, cv2.COLOR_GRAY2BGR)])

# 自适应阈值对比
row2 = np.hstack([cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(thresh_mean, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(thresh_gaussian, cv2.COLOR_GRAY2BGR)])

result = np.vstack([row1, row2])
result = cv2.resize(result, None, fx=0.7, fy=0.7)

cv2.imshow('Thresholding Comparison', result)
print("\n按任意键关闭窗口...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# ==================== 5. 交互式阈值调整 ====================
print("\n5. 交互式阈值调试")

def nothing(x):
    pass

cv2.namedWindow('Threshold Adjustment')

# 创建滑动条
cv2.createTrackbar('Threshold', 'Threshold Adjustment', 127, 255, nothing)
cv2.createTrackbar('Type', 'Threshold Adjustment', 0, 4, nothing)

print("提示：使用滑动条调整阈值，按ESC退出")

while True:
    # 获取滑动条位置
    thresh_val = cv2.getTrackbarPos('Threshold', 'Threshold Adjustment')
    type_val = cv2.getTrackbarPos('Type', 'Threshold Adjustment')

    # 阈值类型
    types = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV,
             cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV]

    # 应用阈值
    ret, thresh = cv2.threshold(gray, thresh_val, 255, types[type_val])

    # 显示结果
    display = np.hstack([cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR),
                        cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)])
    cv2.imshow('Threshold Adjustment', display)

    # 按ESC退出
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()

# ==================== 6. 保存结果 ====================
print("\n6. 保存结果 (已禁用)")

# 保存功能已禁用，如需保存请取消以下注释
# cv2.imwrite('threshold_manual.jpg', thresh_manual)
# cv2.imwrite('threshold_otsu.jpg', thresh_otsu)
# cv2.imwrite('threshold_adaptive_mean.jpg', thresh_mean)
# cv2.imwrite('threshold_adaptive_gaussian.jpg', thresh_gaussian)
print("  [提示] 图片保存功能已禁用，避免生成多余文件")

print("\n程序运行完成！")
