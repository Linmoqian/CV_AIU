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
OpenCV示例：形态学操作

学习目标:
    1. 掌握腐蚀和膨胀操作
    2. 学会开运算和闭运算
    3. 理解形态学梯度的应用
    4. 掌握顶帽和黑帽操作
"""

import cv2
import numpy as np

print("形态学操作")

# 创建测试图像（二值图）
test_img = np.zeros((400, 600, 3), dtype=np.uint8)
test_img[:] = (255, 255, 255)

# 绘制一些形状
cv2.rectangle(test_img, (50, 50), (200, 150), (0, 0, 0), -1)
cv2.circle(test_img, (350, 100), 50, (0, 0, 0), -1)
cv2.rectangle(test_img, (100, 200), (250, 300), (0, 0, 0), 3)
cv2.circle(test_img, (450, 250), 60, (0, 0, 0), 3)

# 添加噪声
for _ in range(100):
    x = np.random.randint(0, 600)
    y = np.random.randint(0, 400)
    cv2.circle(test_img, (x, y), 2, (0, 0, 0), -1)

# 转灰度
gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

# 二值化
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

print("\n测试图像已创建")

# ==================== 1. 腐蚀 ====================
print("\n1. 腐蚀操作")

kernel = np.ones((5, 5), np.uint8)

# 腐蚀1次
erosion_1 = cv2.erode(binary, kernel, iterations=1)
print("  [OK] 腐蚀 1次")

# 腐蚀3次
erosion_3 = cv2.erode(binary, kernel, iterations=3)
print("  [OK] 腐蚀 3次")

# ==================== 2. 膨胀 ====================
print("\n2. 膨胀操作")

# 膨胀1次
dilation_1 = cv2.dilate(binary, kernel, iterations=1)
print("  [OK] 膨胀 1次")

# 膨胀3次
dilation_3 = cv2.dilate(binary, kernel, iterations=3)
print("  [OK] 膨胀 3次")

# ==================== 3. 开运算 ====================
print("\n3. 开运算（先腐蚀后膨胀）")

opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
print("  [OK] 开运算")

# 创建带噪声的图像
noisy = binary.copy()
# 添加白噪声
for _ in range(200):
    x = np.random.randint(0, 600)
    y = np.random.randint(0, 400)
    cv2.circle(noisy, (x, y), 2, 255, -1)

opening_noise = cv2.morphologyEx(noisy, cv2.MORPH_OPEN, kernel)
print("  [OK] 开运算去噪")

# ==================== 4. 闭运算 ====================
print("\n4. 闭运算（先膨胀后腐蚀）")

closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
print("  [OK] 闭运算")

# 创建有孔洞的图像
with_holes = binary.copy()
cv2.circle(with_holes, (100, 100), 20, 255, -1)
cv2.circle(with_holes, (350, 100), 15, 255, -1)

closing_holes = cv2.morphologyEx(with_holes, cv2.MORPH_CLOSE, kernel)
print("  [OK] 闭运算填充孔洞")

# ==================== 5. 形态学梯度 ====================
print("\n5. 形态学梯度")

gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
print("  [OK] 形态学梯度")

# ==================== 6. 顶帽和黑帽 ====================
print("\n6. 顶帽和黑帽")

# 创建亮斑点图像
tophat_img = binary.copy()
cv2.circle(tophat_img, (500, 350), 30, 255, -1)

tophat = cv2.morphologyEx(tophat_img, cv2.MORPH_TOPHAT, kernel)
print("  [OK] 顶帽（提取亮斑点）")

blackhat = cv2.morphologyEx(tophat_img, cv2.MORPH_BLACKHAT, kernel)
print("  [OK] 黑帽（提取暗斑点）")

# ==================== 7. 对比显示 ====================
print("\n7. 显示结果")

# 腐蚀和膨胀对比
row1 = np.hstack([cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(erosion_1, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(dilation_1, cv2.COLOR_GRAY2BGR)])

# 开运算和闭运算对比
row2 = np.hstack([cv2.cvtColor(opening, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(closing, cv2.COLOR_GRAY2BGR),
                  cv2.cvtColor(gradient, cv2.COLOR_GRAY2BGR)])

result = np.vstack([row1, row2])
result = cv2.resize(result, None, fx=0.6, fy=0.6)

cv2.imshow('Morphological Operations', result)
print("\n按任意键继续...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# 去噪效果对比
row = np.hstack([cv2.cvtColor(noisy, cv2.COLOR_GRAY2BGR),
                cv2.cvtColor(opening_noise, cv2.COLOR_GRAY2BGR)])
row = cv2.resize(row, None, fx=0.8, fy=0.8)

cv2.imshow('Noise Removal', row)
print("按任意键继续...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# ==================== 8. 实际应用示例 ====================
print("\n8. 实际应用：文字区域提取")

# 创建文字图像
text_img = np.zeros((300, 600, 3), dtype=np.uint8)
text_img[:] = (255, 255, 255)
cv2.putText(text_img, 'OpenCV Morphology', (50, 150),
           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

text_gray = cv2.cvtColor(text_img, cv2.COLOR_BGR2GRAY)
ret, text_binary = cv2.threshold(text_gray, 127, 255, cv2.THRESH_BINARY_INV)

# 水平膨胀（连接字符）
kernel_horiz = np.ones((1, 15), np.uint8)
text_dilated = cv2.dilate(text_binary, kernel_horiz, iterations=1)

# 查找轮廓
contours, _ = cv2.findContours(text_dilated, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

# 绘制矩形框
result_text = text_img.copy()
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 50 and h > 20:
        cv2.rectangle(result_text, (x, y), (x + w, y + h), (0, 255, 0), 2)

# 显示结果
row = np.hstack([text_img, result_text])
cv2.imshow('Text Detection', row)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ==================== 9. 保存结果 ====================
print("\n9. 保存结果 (已禁用)")

# 保存功能已禁用，如需保存请取消以下注释
# cv2.imwrite('morphology_erosion.jpg', erosion_1)
# cv2.imwrite('morphology_dilation.jpg', dilation_1)
# cv2.imwrite('morphology_opening.jpg', opening)
# cv2.imwrite('morphology_closing.jpg', closing)
# cv2.imwrite('morphology_gradient.jpg', gradient)
print("  [提示] 图片保存功能已禁用，避免生成多余文件")

print("\n程序运行完成！")
