# Task 5: 形态学操作

## 📚 学习目标

通过完成本任务，你将掌握：
- ✅ 理解形态学操作的基本原理（腐蚀、膨胀）
- ✅ 掌握基本的形态学操作（腐蚀、膨胀）
- ✅ 掌握组合形态学操作（开运算、闭运算、形态学梯度、顶帽、黑帽）
- ✅ 理解结构元素（核）的设计和选择
- ✅ 掌握形态学操作的实际应用（去噪、边缘检测、骨架化）
- ✅ 实现硬币计数等实际项目
- ✅ 应用形态学操作填充孔洞
- ✅ 理解不同形态学操作的适用场景
- ✅ 学会评估和优化形态学处理效果

## 🎯 任务概述

本任务要求你掌握图像形态学操作技术，这是基于形状的图像处理方法。形态学操作广泛应用于图像去噪、边缘提取、物体分割、骨架提取等场景。你将实现8种基本的形态学操作，并将它们应用到实际项目中，如硬币计数、孔洞填充等。

**预计时间：** 60-90 分钟
**难度：** ★★★

## 📋 前置知识

在开始之前，确保你已经：
- [ ] 完成了 [Task 1: 图像基本操作](../task-01/README.md)
- [ ] 完成了 [Task 4: 图像阈值处理](../task-04/README.md)
- [ ] 阅读 [07-形态学操作](../../docs/07-形态学操作.md)
- [ ] 理解二值图像的概念
- [ ] 理解卷积和结构元素的基本概念

## 🔧 开发环境

```bash
# 确保已安装必要的库
pip install opencv-python numpy matplotlib

# 测试图片位置
../../assets/sample-images/
```

**推荐测试图像：**
- `shapes/circles.jpg` - 圆形图案
- `shapes/coins.jpg` - 硬币图像
- `basic/landscape.jpg` - 普通风景图（转二值后测试）
- 或自行拍摄包含明显形状的图片

## 📝 任务要求

### 1. 基本形态学操作：腐蚀与膨胀

**目标：** 掌握腐蚀和膨胀操作的原理和效果

**要求：**
1. **腐蚀操作（Erosion）**
   - 使用 `cv2.erode()` 实现
   - 尝试不同的核大小（3x3, 5x5, 7x7）
   - 尝试不同的核形状（矩形、十字形、椭圆形）
   - 保存结果为 `morphology_erode.jpg`
   - 观察腐蚀对白色区域的影响

2. **膨胀操作（Dilation）**
   - 使用 `cv2.dilate()` 实现
   - 尝试不同的核大小和形状
   - 保存结果为 `morphology_dilate.jpg`
   - 对比腐蚀和膨胀的相反效果

3. **创建对比图**
   - 将原图、腐蚀、膨胀结果并排显示
   - 添加文字标签说明
   - 保存为 `morphology_basic_comparison.jpg`

**核心代码：**
```python
import cv2
import numpy as np
import sys
import os

# 添加 utils 路径以支持中文路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

# 读取图像并转为二值图
img_path = get_image_path('sample-images/shapes/circles.jpg')
img = imread_chinese(img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("错误：图像读取失败！")
    sys.exit(1)

# 二值化（确保是黑白二值图）
ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

print(f"原始图像尺寸: {binary.shape}")
print(f"像素范围: [{binary.min)

# ==================== 创建结构元素 ====================
# 形态学操作需要结构元素（核），不同形状有不同效果

# 1. 矩形核（最常用）
kernel_rect_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
kernel_rect_5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
kernel_rect_7 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))

print("\n矩形核 5x5:")
print(kernel_rect_5)

# 2. 十字形核（保留十字形结构）
kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
print("\n十字形核 5x5:")
print(kernel_cross)

# 3. 椭圆形核（更平滑）
kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
print("\n椭圆形核 5x5:")
print(kernel_ellipse)

# ==================== 腐蚀操作 ====================
print("\n[1] 腐蚀操作（Erosion）...")

# 腐蚀：白色区域缩小，黑色区域扩大
# 效果：去除小的白色噪声，断开连接的物体

erode_3 = cv2.erode(binary, kernel_rect_3, iterations=1)
erode_5 = cv2.erode(binary, kernel_rect_5, iterations=1)
erode_7 = cv2.erode(binary, kernel_rect_7, iterations=1)

cv2.imwrite('morphology_erode_3x3.jpg', erode_3)
cv2.imwrite('morphology_erode_5x5.jpg', erode_5)
cv2.imwrite('morphology_erode_7x7.jpg', erode_7)

print("  [OK] 腐蚀操作完成")
print("  - 核大小 3x3: morphology_erode_3x3.jpg")
print("  - 核大小 5x5: morphology_erode_5x5.jpg")
print("  - 核大小 7x7: morphology_erode_7x7.jpg")

# 统计腐蚀前后白色像素数量
white_before = np.count_nonzero(binary)
white_after_3 = np.count_nonzero(erode_3)
white_after_5 = np.count_nonzero(erode_5)
white_after_7 = np.count_nonzero(erode_7)

print(f"\n  白色像素统计:")
print(f"  - 腐蚀前: {white_before} 个")
print(f"  - 腐蚀后 (3x3): {white_after_3} 个 ({white_after_3/white_before*100:.1f}%)")
print(f"  - 腐蚀后 (5x5): {white_after_5} 个 ({white_after_5/white_before*100:.1f}%)")
print(f"  - 腐蚀后 (7x7): {white_after_7} 个 ({white_after_7/white_before*100:.1f}%)")

# ==================== 膨胀操作 ====================
print("\n[2] 膨胀操作（Dilation）...")

# 膨胀：白色区域扩大，黑色区域缩小
# 效果：填充小的黑色空洞，连接邻近的物体

dilate_3 = cv2.dilate(binary, kernel_rect_3, iterations=1)
dilate_5 = cv2.dilate(binary, kernel_rect_5, iterations=1)
dilate_7 = cv2.dilate(binary, kernel_rect_7, iterations=1)

cv2.imwrite('morphology_dilate_3x3.jpg', dilate_3)
cv2.imwrite('morphology_dilate_5x5.jpg', dilate_5)
cv2.imwrite('morphology_dilate_7x7.jpg', dilate_7)

print("  [OK] 膨胀操作完成")
print("  - 核大小 3x3: morphology_dilate_3x3.jpg")
print("  - 核大小 5x5: morphology_dilate_5x5.jpg")
print("  - 核大小 7x7: morphology_dilate_7x7.jpg")

# 统计膨胀前后白色像素数量
white_after_dilate_3 = np.count_nonzero(dilate_3)
white_after_dilate_5 = np.count_nonzero(dilate_5)
white_after_dilate_7 = np.count_nonzero(dilate_7)

print(f"\n  白色像素统计:")
print(f"  - 膨胀前: {white_before} 个")
print(f"  - 膨胀后 (3x3): {white_after_dilate_3} 个 ({white_after_dilate_3/white_before*100:.1f}%)")
print(f"  - 膨胀后 (5x5): {white_after_dilate_5} 个 ({white_after_dilate_5/white_before*100:.1f}%)")
print(f"  - 膨胀后 (7x7): {white_after_dilate_7} 个 ({white_after_dilate_7/white_before*100:.1f}%)")

# ==================== 不同形状核的效果 ====================
print("\n[3] 不同形状核的效果对比...")

# 使用相同大小的不同核进行腐蚀
erode_cross = cv2.erode(binary, kernel_cross, iterations=1)
erode_ellipse = cv2.erode(binary, kernel_ellipse, iterations=1)

cv2.imwrite('morphology_erode_cross.jpg', erode_cross)
cv2.imwrite('morphology_erode_ellipse.jpg', erode_ellipse)

print("  [OK] 不同核形状对比完成")
print("  - 十字形核: morphology_erode_cross.jpg")
print("  - 椭圆形核: morphology_erode_ellipse.jpg")

# 创建对比图
def add_title(image, title):
    """在图像上添加标题"""
    img_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.putText(img_bgr, title, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return img_bgr

titles = ['Original', 'Erode 3x3', 'Erode 5x5', 'Dilate 3x3', 'Dilate 5x5', 'Cross Kernel']
images = [binary, erode_3, erode_5, dilate_3, dilate_5, erode_cross]

labeled_images = []
for img, title in zip(images, titles):
    labeled = add_title(img, title)
    labeled_images.append(labeled)

# 组合图像（2行3列）
row1 = np.hstack(labeled_images[:3])
row2 = np.hstack(labeled_images[3:])
comparison = np.vstack([row1, row2])
comparison = cv2.resize(comparison, None, fx=0.6, fy=0.6)
cv2.imwrite('morphology_basic_comparison.jpg', comparison)

print("\n  [OK] 基本操作对比图已保存: morphology_basic_comparison.jpg")
```

**原理解析：**

**腐蚀（Erosion）：**
- 原理：用结构元素的中心滑动图像，如果结构元素覆盖的所有像素都是白色，则中心像素设为白色，否则设为黑色
- 效果：白色区域缩小（被"腐蚀"），黑色区域扩大
- 用途：
  - 去除小的白色噪声
  - 断开连接在一起的物体
  - 细化白色区域

**膨胀（Dilation）：**
- 原理：用结构元素的中心滑动图像，如果结构元素覆盖的任意像素是白色，则中心像素设为白色
- 效果：白色区域扩大（被"膨胀"），黑色区域缩小
- 用途：
  - 填充小的黑色空洞
  - 连接邻近的物体
  - 增强白色区域

**提示：**
- 腐蚀和膨胀是相反的操作
- 核越大，效果越明显
- iterations 参数控制操作重复次数
- 核形状影响处理结果：矩形核最强，椭圆形核较平滑，十字形核保留方向性
- 可以多次应用相同操作增强效果

---

### 2. 组合形态学操作

**目标：** 掌握开运算、闭运算、形态学梯度、顶帽、黑帽等组合操作

**要求：**
1. **开运算（Opening Operation）**
   - 使用 `cv2.morphologyEx()` 配合 `cv2.MORPH_OPEN`
   - 理解：先腐蚀后膨胀
   - 保存结果为 `morphology_opening.jpg`
   - 分析其去噪效果

2. **闭运算（Closing Operation）**
   - 使用 `cv2.morphologyEx()` 配合 `cv2.MORPH_CLOSE`
   - 理解：先膨胀后腐蚀
   - 保存结果为 `morphology_closing.jpg`
   - 分析其填充效果

3. **形态学梯度（Morphological Gradient）**
   - 使用 `cv2.MORPH_GRADIENT`
   - 理解：膨胀图 - 腐蚀图
   - 保存结果为 `morphology_gradient.jpg`
   - 对比 Sobel 和 Canny 边缘检测

4. **顶帽变换（Top Hat）**
   - 使用 `cv2.MORPH_TOPHAT`
   - 理解：原图 - 开运算结果
   - 保存结果为 `morphology_tophat.jpg`
   - 观察其提取亮细节的能力

5. **黑帽变换（Black Hat）**
   - 使用 `cv2.MORPH_BLACKHAT`
   - 理解：闭运算结果 - 原图
   - 保存结果为 `morphology_blackhat.jpg`
   - 观察其提取暗细节的能力

**完整代码框架：**
```python
import cv2
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

# 读取图像
img_path = get_image_path('sample-images/shapes/circles.jpg')
img = imread_chinese(img_path, cv2.IMREAD_GRAYSCALE)

ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# 创建结构元素
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

print("=" * 60)
print("Task 5: 形态学操作 - 组合操作")
print("=" * 60)

# ==================== 1. 开运算 ====================
print("\n[1] 开运算（Opening Operation）...")
print("  原理: 先腐蚀后膨胀")
print("  效果: 去除小的白色噪声，断开连接的物体")

# 开运算：先腐蚀后膨胀
# 用途：去除小的白色噪声，保持物体大致形状
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
cv2.imwrite('morphology_opening.jpg', opening)

# 统计
white_before = np.count_nonzero(binary)
white_opening = np.count_nonzero(opening)
print(f"  白色像素: {white_before} -> {white_opening} ({white_opening/white_before*100:.1f}%)")
print(f"  [OK] 开运算结果已保存: morphology_opening.jpg")

# 对比单独的腐蚀和膨胀
eroded = cv2.erode(binary, kernel, iterations=1)
dilated_after_erode = cv2.dilate(eroded, kernel, iterations=1)

# 验证：开运算 = 先腐蚀后膨胀
print(f"  验证: 开运算 == 先腐蚀后膨胀: {np.array_equal(opening, dilated_after_erode)}")

# ==================== 2. 闭运算 ====================
print("\n[2] 闭运算（Closing Operation）...")
print("  原理: 先膨胀后腐蚀")
print("  效果: 填充小的黑色空洞，连接邻近的物体")

# 闭运算：先膨胀后腐蚀
# 用途：填充小的黑色空洞，连接断裂的物体
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
cv2.imwrite('morphology_closing.jpg', closing)

# 统计
white_closing = np.count_nonzero(closing)
print(f"  白色像素: {white_before} -> {white_closing} ({white_closing/white_before*100:.1f}%)")
print(f"  [OK] 闭运算结果已保存: morphology_closing.jpg")

# 验证：闭运算 = 先膨胀后腐蚀
dilated = cv2.dilate(binary, kernel, iterations=1)
eroded_after_dilate = cv2.erode(dilated, kernel, iterations=1)
print(f"  验证: 闭运算 == 先膨胀后腐蚀: {np.array_equal(closing, eroded_after_dilate)}")

# ==================== 3. 形态学梯度 ====================
print("\n[3] 形态学梯度（Morphological Gradient）...")
print("  原理: 膨胀图 - 腐蚀图")
print("  效果: 提取物体边缘")

# 形态学梯度：膨胀 - 腐蚀
# 用途：提取物体边缘，比 Canny 更简单
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
cv2.imwrite('morphology_gradient.jpg', gradient)

# 手动计算验证
eroded = cv2.erode(binary, kernel, iterations=1)
dilated = cv2.dilate(binary, kernel, iterations=1)
gradient_manual = cv2.subtract(dilated, eroded)

print(f"  验证: 形态学梯度 == 膨胀 - 腐蚀: {np.array_equal(gradient, gradient_manual)}")
print(f"  边缘像素数: {np.count_nonzero(gradient)}")
print(f"  [OK] 形态学梯度已保存: morphology_gradient.jpg")

# ==================== 4. 顶帽变换 ====================
print("\n[4] 顶帽变换（Top Hat）...")
print("  原理: 原图 - 开运算结果")
print("  效果: 提取比周围区域亮的细节")

# 顶帽：原图 - 开运算
# 用途：提取亮的细节（小的白色区域）
tophat = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, kernel)
cv2.imwrite('morphology_tophat.jpg', tophat)

# 手动计算验证
tophat_manual = cv2.subtract(binary, opening)
print(f"  验证: 顶帽 == 原图 - 开运算: {np.array_equal(tophat, tophat_manual)}")
print(f"  亮细节像素数: {np.count_nonzero(tophat)}")
print(f"  [OK] 顶帽变换已保存: morphology_tophat.jpg")

# ==================== 5. 黑帽变换 ====================
print("\n[5] 黑帽变换（Black Hat）...")
print("  原理: 闭运算结果 - 原图")
print("  效果: 提取比周围区域暗的细节")

# 黑帽：闭运算 - 原图
# 用途：提取暗的细节（小的黑色区域）
blackhat = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, kernel)
cv2.imwrite('morphology_blackhat.jpg', blackhat)

# 手动计算验证
blackhat_manual = cv2.subtract(closing, binary)
print(f"  验证: 黑帽 == 闭运算 - 原图: {np.array_equal(blackhat, blackhat_manual)}")
print(f"  暗细节像素数: {np.count_nonzero(blackhat)}")
print(f"  [OK] 黑帽变换已保存: morphology_blackhat.jpg")

# ==================== 创建综合对比图 ====================
print("\n[6] 创建综合对比图...")

def add_title(image, title):
    """在图像上添加标题"""
    img_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.putText(img_bgr, title, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return img_bgr

titles = ['Original', 'Opening', 'Closing', 'Gradient', 'Top Hat', 'Black Hat']
images = [binary, opening, closing, gradient, tophat, blackhat]

labeled_images = []
for img, title in zip(images, titles):
    labeled = add_title(img, title)
    labeled_images.append(labeled)

# 组合图像（2行3列）
row1 = np.hstack(labeled_images[:3])
row2 = np.hstack(labeled_images[3:])
comparison = np.vstack([row1, row2])
comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
cv2.imwrite('morphology_all_operations.jpg', comparison)

print(f"  [OK] 综合对比图已保存: morphology_all_operations.jpg")

# ==================== 效果总结 ====================
print("\n" + "=" * 60)
print("形态学操作效果总结")
print("=" * 60)
print(f"{'操作':<15} {'原理':<20} {'主要用途':<25}")
print("-" * 60)
print(f"{'腐蚀':<15} {'白色区域缩小':<20} {'去噪、断开物体':<25}")
print(f"{'膨胀':<15} {'白色区域扩大':<20} {'填充、连接物体':<25}")
print(f"{'开运算':<15} {'先腐蚀后膨胀':<20} {'去白噪、保持形状':<25}")
print(f"{'闭运算':<15} {'先膨胀后腐蚀':<20} {'填黑洞、连接断裂':<25}")
print(f"{'形态学梯度':<15} {'膨胀 - 腐蚀':<20} {'提取边缘':<25}")
print(f"{'顶帽':<15} {'原图 - 开运算':<20} {'提取亮细节':<25}")
print(f"{'黑帽':<15} {'闭运算 - 原图':<20} {'提取暗细节':<25}")
print("=" * 60)
```

**6种形态学操作详解：**

| 操作 | 公式 | 效果 | 主要用途 | 适用场景 |
|------|------|------|---------|---------|
| **腐蚀** | A ⊖ B | 白色区域缩小 | 去除小的白色噪声 | 去噪、断开物体 |
| **膨胀** | A ⊕ B | 白色区域扩大 | 填充小的黑色空洞 | 填充、连接物体 |
| **开运算** | (A ⊖ B) ⊕ B | 去除小白点，保持大形状 | 去噪、断开连接 | 噪声去除 |
| **闭运算** | (A ⊕ B) ⊖ B | 填充小黑洞，连接物体 | 填充孔洞、连接断裂 | 孔洞填充 |
| **梯度** | (A ⊕ B) - (A ⊖ B) | 提取边缘 | 边缘检测 | 边缘提取 |
| **顶帽** | A - (A ⊖ B) ⊕ B | 提取亮细节 | 提取小的亮区域 | 亮度不均校正 |
| **黑帽** | (A ⊕ B) ⊖ B - A | 提取暗细节 | 提取小的暗区域 | 暗区域检测 |

**应用场景选择：**

```
图像有白色噪声 → 开运算
图像有黑色孔洞 → 闭运算
需要提取边缘 → 形态学梯度
需要提取亮细节 → 顶帽变换
需要提取暗细节 → 黑帽变换
需要断开物体 → 腐蚀
需要连接物体 → 膨胀
```

**提示：**
- 开运算和闭运算不会显著改变物体大小
- 开运算适合去除小的白色噪声
- 闭运算适合填充小的黑色孔洞
- 形态学梯度比 Canny 更简单，但边缘较粗
- 顶帽和黑帽用于提取局部细节
- 核大小需要根据噪声/细节大小调整

---

### 3. 形态学应用：去噪与边缘检测

**目标：** 将形态学操作应用到实际场景中

**要求：**
1. **噪声去除实验**
   - 对含噪图像应用开运算去除白色噪声
   - 对含噪图像应用闭运算去除黑色噪声
   - 对比处理前后的效果
   - 保存结果为 `morphology_denoising_result.jpg`

2. **边缘检测对比**
   - 应用形态学梯度检测边缘
   - 对比 Sobel 边缘检测
   - 对比 Canny 边缘检测
   - 分析各自的优缺点
   - 保存结果为 `morphology_edge_comparison.jpg`

3. **迭代形态学操作**
   - 多次应用腐蚀操作实现骨架化
   - 多次应用膨胀操作实现区域增长
   - 保存中间结果观察变化

**完整代码框架：**
```python
import cv2
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

print("=" * 60)
print("形态学操作应用：去噪与边缘检测")
print("=" * 60)

# ==================== 1. 噪声去除 ====================
print("\n[1] 形态学去噪实验...")

# 创建含噪图像（或读取已有的含噪图像）
img_path = get_image_path('sample-images/basic/landscape.jpg')
img = imread_chinese(img_path, cv2.IMREAD_GRAYSCALE)

# 二值化
ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# 添加噪声（如果没有现成的含噪图像）
def add_noise(image, noise_type='salt_pepper', amount=0.02):
    """
    为图像添加噪声

    参数:
        image: 输入二值图像
        noise_type: 'salt_pepper' 或 'gaussian'
        amount: 噪声密度
    """
    noisy = image.copy()
    total_pixels = image.size

    if noise_type == 'salt_pepper':
        # 添加椒盐噪声
        num_salt = int(amount * total_pixels * 0.5)
        salt_coords = [np.random.randint(0, i-1, num_salt) for i in image.shape]
        noisy[salt_coords[0], salt_coords[1]] = 255

        num_pepper = int(amount * total_pixels * 0.5)
        pepper_coords = [np.random.randint(0, i-1, num_pepper) for i in image.shape]
        noisy[pepper_coords[0], pepper_coords[1]] = 0

    return noisy

# 添加椒盐噪声
noisy = add_noise(binary, 'salt_pepper', 0.05)
cv2.imwrite('morphology_noisy_input.jpg', noisy)

# 形态学去噪
kernel_small = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
kernel_medium = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 去除白色噪声（先用开运算）
opening_small = cv2.morphologyEx(noisy, cv2.MORPH_OPEN, kernel_small)
opening_medium = cv2.morphologyEx(noisy, cv2.MORPH_OPEN, kernel_medium)

# 填充黑色噪声（再用闭运算）
closing_small = cv2.morphologyEx(opening_small, cv2.MORPH_CLOSE, kernel_small)
closing_medium = cv2.morphologyEx(opening_medium, cv2.MORPH_CLOSE, kernel_medium)

# 保存结果
cv2.imwrite('morphology_denoise_opening_small.jpg', opening_small)
cv2.imwrite('morphology_denoise_opening_medium.jpg', opening_medium)
cv2.imwrite('morphology_denoise_final_small.jpg', closing_small)
cv2.imwrite('morphology_denoise_final_medium.jpg', closing_medium)

# 创建对比图
def add_title(image, title):
    img_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.putText(img_bgr, title, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return img_bgr

titles = ['Noisy', 'Opening(3x3)', 'Opening(5x5)', 'Final(3x3)', 'Final(5x5)', 'Original']
images = [noisy, opening_small, opening_medium, closing_small, closing_medium, binary]

labeled_images = []
for img, title in zip(images, titles):
    labeled = add_title(img, title)
    labeled_images.append(labeled)

row1 = np.hstack(labeled_images[:3])
row2 = np.hstack(labeled_images[3:])
comparison = np.vstack([row1, row2])
comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
cv2.imwrite('morphology_denoising_result.jpg', comparison)

print("  [OK] 形态学去噪完成")
print("  - 含噪图像: morphology_noisy_input.jpg")
print("  - 去噪对比: morphology_denoising_result.jpg")

# ==================== 2. 边缘检测对比 ====================
print("\n[2] 边缘检测方法对比...")

# 形态学梯度
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
morph_gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

# Sobel 边缘检测
sobelx = cv2.Sobel(binary, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(binary, cv2.CV_64F, 0, 1, ksize=3)
sobelx = np.uint8(np.absolute(sobelx))
sobely = np.uint8(np.absolute(sobely))
sobel_combined = cv2.add(sobelx, sobely)

# Canny 边缘检测
canny = cv2.Canny(binary, 50, 150)

# 保存结果
cv2.imwrite('morphology_edge_morph.jpg', morph_gradient)
cv2.imwrite('morphology_edge_sobel.jpg', sobel_combined)
cv2.imwrite('morphology_edge_canny.jpg', canny)

# 创建对比图
titles = ['Original', 'Morph Gradient', 'Sobel', 'Canny']
images = [binary, morph_gradient, sobel_combined, canny]

labeled_images = []
for img, title in zip(images, titles):
    labeled = add_title(img, title)
    labeled_images.append(labeled)

comparison = np.hstack(labeled_images)
comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
cv2.imwrite('morphology_edge_comparison.jpg', comparison)

print("  [OK] 边缘检测对比完成")
print("  - 形态学梯度: morphology_edge_morph.jpg")
print("  - Sobel: morphology_edge_sobel.jpg")
print("  - Canny: morphology_edge_canny.jpg")
print("  - 对比图: morphology_edge_comparison.jpg")

# 统计边缘像素
edge_pixels_morph = np.count_nonzero(morph_gradient)
edge_pixels_sobel = np.count_nonzero(sobel_combined)
edge_pixels_canny = np.count_nonzero(canny)

print(f"\n  边缘像素统计:")
print(f"  - 形态学梯度: {edge_pixels_morph} 个")
print(f"  - Sobel: {edge_pixels_sobel} 个")
print(f"  - Canny: {edge_pixels_canny} 个")

# ==================== 3. 迭代形态学操作 ====================
print("\n[3] 迭代形态学操作...")

# 3.1 迭代腐蚀实现骨架化
print("  迭代腐蚀（骨架化）...")
skeleton = binary.copy()
kernel_small = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

skeleton_images = []
for i in range(10):
    skeleton = cv2.erode(skeleton, kernel_small, iterations=1)
    skeleton_images.append(skeleton.copy())
    cv2.imwrite(f'morphology_erode_iter_{i+1}.jpg', skeleton)

    # 统计白色像素
    white_pixels = np.count_nonzero(skeleton)
    print(f"    迭代 {i+1}: {white_pixels} 个白色像素")

# 创建骨架化过程图
row1 = np.hstack([skeleton_images[0], skeleton_images[2], skeleton_images[4]])
row2 = np.hstack([skeleton_images[6], skeleton_images[8], skeleton_images[9]])
skeleton_process = np.vstack([row1, row2])
skeleton_process = cv2.resize(skeleton_process, None, fx=0.4, fy=0.4)
cv2.imwrite('morphology_skeleton_process.jpg', skeleton_process)

print("  [OK] 骨架化过程图已保存: morphology_skeleton_process.jpg")

# 3.2 迭代膨胀实现区域增长
print("  迭代膨胀（区域增长）...")
dilated = binary.copy()

dilated_images = []
for i in range(5):
    dilated = cv2.dilate(dilated, kernel_small, iterations=1)
    dilated_images.append(dilated.copy())
    cv2.imwrite(f'morphology_dilate_iter_{i+1}.jpg', dilated)

    # 统计白色像素
    white_pixels = np.count_nonzero(dilated)
    print(f"    迭代 {i+1}: {white_pixels} 个白色像素")

# 创建区域增长过程图
row1 = np.hstack([binary] + dilated_images[:2])
row2 = np.hstack(dilated_images[2:5])
dilate_process = np.vstack([row1, row2])
dilate_process = cv2.resize(dilate_process, None, fx=0.4, fy=0.4)
cv2.imwrite('morphology_dilate_process.jpg', dilate_process)

print("  [OK] 区域增长过程图已保存: morphology_dilate_process.jpg")

print("\n" + "=" * 60)
print("形态学应用实验完成！")
print("=" * 60)
```

**去噪效果分析：**

| 噪声类型 | 形态学操作 | 核大小选择 | 效果 |
|---------|-----------|-----------|------|
| 白色噪声（椒噪声） | 开运算 | 核大小 ≈ 噪声大小 × 2 | 完全去除 |
| 黑色噪声（盐噪声） | 闭运算 | 核大小 ≈ 噪声大小 × 2 | 完全填充 |
| 混合噪声 | 开运算 + 闭运算 | 先小核后大核 | 效果最佳 |

**边缘检测对比：**

| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **形态学梯度** | 简单快速，边缘连续 | 边缘较粗，噪声敏感 | 简单场景，快速预览 |
| **Sobel** | 计算快速，有方向性 |
| **Canny** | 边缘细，抗噪能力强 | 需要调参，计算较慢 | 精确边缘检测 |

**提示：**
- 去噪时核大小应约为噪声大小的 2 倍
- 复杂噪声可以组合多次开运算和闭运算
- 形态学梯度适合快速预览边缘
- 迭代腐蚀可以逐渐细化物体
- 迭代膨胀可以逐渐扩大物体

---

### 4. 实际项目：硬币计数

**目标：** 应用形态学操作实现硬币计数系统

**要求：**
1. **完整的硬币计数流程**
   - 读取硬币图像
   - 预处理（灰度化、阈值处理）
   - 形态学去噪
   - 查找轮廓
   - 统计硬币数量
   - 在原图上标记硬币

2. **不同大小的硬币分类**
   - 根据面积区分不同面值
   - 统计每种硬币的数量
   - 计算总金额

3. **可视化结果**
   - 绘制检测到的硬币边界
   - 标记硬币编号
   - 显示统计信息
   - 保存结果图像

**完整代码框架：**
```python
import cv2
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

def count_coins(image_path):
    """
    硬币计数系统

    流程:
    1. 读取图像
    2. 预处理（灰度、阈值）
    3. 形态学去噪
    4. 查找轮廓
    5. 统计和分类
    6. 可视化标记
    """

    print("=" * 60)
    print("硬币计数系统")
    print("=" * 60)

    # 1. 读取图像
    print("\n[1] 读取图像...")
    img = imread_chinese(image_path)
    if img is None:
        print("  [ERROR] 图像读取失败！")
        return None

    print(f"  [OK] 图像尺寸: {img.shape}")

    # 2. 预处理
    print("\n[2] 图像预处理...")

    # 转灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"  [OK] 灰度转换完成")

    # 高斯滤波降噪
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    print(f"  [OK] 高斯滤波完成")

    # 自适应阈值
    binary = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,  # 使用 INV 使硬币为白色
        11, 2
    )
    cv2.imwrite('coins_binary.jpg', binary)
    print(f"  [OK] 自适应阈值完成")

    # 3. 形态学去噪
    print("\n[3] 形态学去噪...")

    # 闭运算：填充硬币内部的小黑洞
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_close)
    print(f"  [OK] 闭运算完成（填充孔洞）")

    # 开运算：去除背景噪声
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel_open)
    cv2.imwrite('coins_morphology.jpg', opening)
    print(f"  [OK] 开运算完成（去除噪声）")

    # 再次闭运算确保硬币完整
    final = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_close)
    cv2.imwrite('coins_final_binary.jpg', final)

    # 4. 查找轮廓
    print("\n[4] 查找硬币轮廓...")

    contours, hierarchy = cv2.findContours(
        final,
        cv2.RETR_EXTERNAL,  # 只检测外轮廓
        cv2.CHAIN_APPROX_SIMPLE  # 简化轮廓
    )

    print(f"  检测到 {len(contours)} 个轮廓")

    # 过滤小轮廓（去除噪声）
    min_area = 100  # 最小面积阈值
    coins = []
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > min_area:
            coins.append({
                'id': i,
                'contour': contour,
                'area': area
            })

    print(f"  过滤后剩余 {len(coins)} 个硬币")

    if len(coins) == 0:
        print("  [WARNING] 未检测到硬币！")
        return None

    # 5. 硬币分类（根据面积）
    print("\n[5] 硬币分类...")

    # 统计面积分布
    areas = [coin['area'] for coin in coins]
    min_area = min(areas)
    max_area = max(areas)
    avg_area = sum(areas) / len(areas)

    print(f"  面积范围: {min_area:.0f} - {max_area:.0f}")
    print(f"  平均面积: {avg_area:.0f}")

    # 简单分类（假设只有两种硬币）
    # 实际应用中需要根据具体硬币尺寸调整阈值
    threshold = (min_area + max_area) / 2

    small_coins = [c for c in coins if c['area'] < threshold]
    large_coins = [c for c in coins if c['area'] >= threshold]

    print(f"  小硬币: {len(small_coins)} 个")
    print(f"  大硬币: {len(large_coins)} 个")

    # 6. 可视化标记
    print("\n[6] 可视化标记...")

    result = img.copy()

    # 绘制所有硬币
    for coin in coins:
        contour = coin['contour']

        # 获取边界框
        x, y, w, h = cv2.boundingRect(contour)

        # 计算中心
        center_x = x + w // 2
        center_y = y + h // 2

        # 判断硬币类型
        coin_type = "小" if coin['area'] < threshold else "大"
        color = (0, 255, 0) if coin['area'] < threshold else (0, 0, 255)

        # 绘制轮廓
        cv2.drawContours(result, [contour], -1, color, 2)

        # 绘制边界框
        cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)

        # 绘制中心点
        cv2.circle(result, (center_x, center_y), 3, color, -1)

        # 标注编号
        cv2.putText(result, f"#{coin['id']}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # 标注面积
        label = f"{coin_type} ({int(coin['area'])})"
        cv2.putText(result, label, (x, y + h + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # 添加统计信息
    info_text = [
        f"Small: {len(small_coins)}",
        f"Large: {len(large_coins)}",
    ]

    for i, text in enumerate(info_text):
        cv2.putText(result, text, (10, 30 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(result, text, (10, 30 + i * 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)

    cv2.imwrite('coins_result.jpg', result)
    print(f"  [OK] 结果已保存: coins_result.jpg")

    # 7. 生成处理过程图
    print("\n[7] 生成处理过程图...")

    # 调整大小以便显示
    h, w = binary.shape
    binary_resized = cv2.resize(binary, (w // 2, h // 2))
    morphology_resized = cv2.resize(final, (w // 2, h // 2))
    result_resized = cv2.resize(result, (w // 2, h // 2))

    # 转换为彩色以便组合
    binary_color = cv2.cvtColor(binary_resized, cv2.COLOR_GRAY2BGR)
    morphology_color = cv2.cvtColor(morphology_resized, cv2.COLOR_GRAY2BGR)

    # 添加标题
    cv2.putText(binary_color, "Binary", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(morphology_color, "After Morphology", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(result_resized, "Detected Coins", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 组合图像
    process = np.hstack([binary_color, morphology_color, result_resized])
    cv2.imwrite('coins_process.jpg', process)
    print(f"  [OK] 处理过程图已保存: coins_process.jpg")

    # 8. 生成报告
    print("\n[8] 生成报告...")

    report = f"""
# 硬币计数报告

## 检测结果
- 总硬币数: {len(coins)} 个
- 小硬币: {len(small_coins)} 个
- 大硬币: {len(large_coins)} 个

## 面积统计
- 最小面积: {min_area:.0f} 像素
- 最大面积: {max_area:.0f} 像素
- 平均面积: {avg_area:.0f} 像素
- 分类阈值: {threshold:.0f} 像素

## 处理参数
- 高斯滤波: 5x5, sigma=0
- 自适应阈值: GAUSSIAN_C, blockSize=11, C=2
- 形态学闭运算: 5x5
- 形态学开运算: 3x3
- 最小硬币面积: {min_area} 像素

## 硬币详情
"""

    for coin in coins:
        coin_type = "小" if coin['area'] < threshold else "大"
        report += f"\n- 硬币 #{coin['id']}: {coin_type}, 面积={int(coin['area'])}\n"

    with open('coins_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"  [OK] 报告已保存: coins_report.txt")

    print("\n" + "=" * 60)
    print("硬币计数完成！")
    print("=" * 60)
    print(f"\n检测结果:")
    print(f"  - 总硬币数: {len(coins)} 个")
    print(f"  - 小硬币: {len(small_coins)} 个")
    print(f"  - 大硬币: {len(large_coins)} 个")

    return {
        'total': len(coins),
        'small': len(small_coins),
        'large': len(large_coins),
        'coins': coins
    }

# 使用示例
if __name__ == "__main__":
    img_path = get_image_path('sample-images/shapes/coins.jpg')
    result = count_coins(img_path)
```

**硬币计数流程图：**

```
输入图像
    ↓
灰度转换
    ↓
高斯滤波（降噪）
    ↓
自适应阈值（二值化）
    ↓
形态学闭运算（填充孔洞）
    ↓
形态学开运算（去除噪声）
    ↓
查找轮廓
    ↓
过滤小轮廓
    ↓
根据面积分类
    ↓
绘制标记和统计
    ↓
输出结果
```

**优化建议：**
- 如果硬币粘连，可以使用分水岭算法
- 如果光照不均，可以使用顶帽变换校正
- 如果硬币有反光，可以使用双边滤波
- 面积阈值需要根据实际硬币尺寸调整

---

## 📦 提交要求

### 必交内容

1. **代码文件**：`task5_solution.py`
   - 包含所有4个任务的实现
   - 代码注释清晰，符合 PEP 8 规范
   - 包含完整的硬币计数系统

2. **保存的图像**（按任务要求命名）：
   ```
   # 任务1：基本形态学操作
   morphology_erode_3x3.jpg
   morphology_erode_5x5.jpg
   morphology_dilate_3x3.jpg
   morphology_dilate_5x5.jpg
   morphology_erode_cross.jpg
   morphology_erode_ellipse.jpg
   morphology_basic_comparison.jpg

   # 任务2：组合形态学操作
   morphology_opening.jpg
   morphology_closing.jpg
   morphology_gradient.jpg
   morphology_tophat.jpg
   morphology_blackhat.jpg
   morphology_all_operations.jpg

   # 任务3：形态学应用
   morphology_noisy_input.jpg
   morphology_denoising_result.jpg
   morphology_edge_comparison.jpg
   morphology_skeleton_process.jpg
   morphology_dilate_process.jpg

   # 任务4：硬币计数
   coins_binary.jpg
   coins_morphology.jpg
   coins_final_binary.jpg
   coins_result.jpg
   coins_process.jpg
   ```

3. **分析报告**：`morphology_analysis_report.txt` 或 `report.md`
   - 对比8种形态学操作的原理和效果
   - 分析不同核形状的影响
   - 总结硬币计数系统的设计和优化
   - 至少 500 字

4. **运行结果截图**：`result_screenshot.png`
   - 显示程序运行的控制台输出
   - 包含统计信息和处理参数

### 提交格式

```
task-05-submission/
├── task5_solution.py               # 你的代码
├── result_screenshot.png           # 运行结果截图
├── morphology_analysis_report.txt   # 分析报告
├── output_images/                   # 输出图像文件夹
│   ├── 基本操作/
│   ├── 组合操作/
│   ├── 应用实验/
│   └── 硬币计数/
└── report.md                       # 实验报告（可选）
```

---

## 💡 完整代码框架

```python
"""
Task 5: 形态学操作
姓名：[你的名字]
学号：[你的学号]
日期：[提交日期]
"""

import cv2
import numpy as np
import sys
import os

# ==================== 配置区 ====================
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

# 图片路径
IMG_PATH = 'sample-images/shapes/circles.jpg'
COINS_PATH = 'sample-images/shapes/coins.jpg'
OUTPUT_DIR = 'output_images'

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 工具函数 ====================
def add_title(image, title):
    """在图像上添加标题"""
    if len(image.shape) == 2:
        img_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        img_bgr = image.copy()

    cv2.putText(img_bgr, title, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return img_bgr

def create_comparison(images, titles, rows, cols):
    """创建对比图"""
    labeled_images = []
    for img, title in zip(images, titles):
        labeled = add_title(img, title)
        labeled_images.append(labeled)

    # 组合成网格
    grid_rows = []
    for i in range(rows):
        start_idx = i * cols
        end_idx = start_idx + cols
        row = np.hstack(labeled_images[start_idx:end_idx])
        grid_rows.append(row)

    return np.vstack(grid_rows)

# ==================== 主程序 ====================
print("=" * 70)
print("Task 5: 形态学操作")
print("=" * 70)

# ==================== 1. 基本形态学操作 ====================
print("\n[1] 基本形态学操作（腐蚀与膨胀）...")

img_path = get_image_path(IMG_PATH)
img = imread_chinese(img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("  [ERROR] 图像读取失败！")
    sys.exit(1)

# 二值化
ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
print(f"  [OK] 图像读取成功: {binary.shape}")

# 创建不同形状的结构元素
kernel_rect_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
kernel_rect_5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# 腐蚀操作
erode_3 = cv2.erode(binary, kernel_rect_3, iterations=1)
erode_5 = cv2.erode(binary, kernel_rect_5, iterations=1)
erode_cross = cv2.erode(binary, kernel_cross, iterations=1)
erode_ellipse = cv2.erode(binary, kernel_ellipse, iterations=1)

# 膨胀操作
dilate_3 = cv2.dilate(binary, kernel_rect_3, iterations=1)
dilate_5 = cv2.dilate(binary, kernel_rect_5, iterations=1)

# 保存结果
cv2.imwrite(f'{OUTPUT_DIR}/morphology_erode_3x3.jpg', erode_3)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_erode_5x5.jpg', erode_5)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_erode_cross.jpg', erode_cross)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_erode_ellipse.jpg', erode_ellipse)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_dilate_3x3.jpg', dilate_3)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_dilate_5x5.jpg', dilate_5)

# 创建对比图
titles = ['Original', 'Erode 3x3', 'Erode 5x5', 'Dilate 3x3', 'Dilate 5x5', 'Cross']
images = [binary, erode_3, erode_5, dilate_3, dilate_5, erode_cross]
comparison = create_comparison(images, titles, 2, 3)
comparison = cv2.resize(comparison, None, fx=0.6, fy=0.6)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_basic_comparison.jpg', comparison)

print(f"  [OK] 基本操作完成")

# 统计
white_orig = np.count_nonzero(binary)
white_erode_3 = np.count_nonzero(erode_3)
white_dilate_3 = np.count_nonzero(dilate_3)
print(f"  白色像素: {white_orig} -> {white_erode_3} (腐蚀) -> {white_dilate_3} (膨胀)")

# ==================== 2. 组合形态学操作 ====================
print("\n[2] 组合形态学操作...")

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 开运算
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# 闭运算
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# 形态学梯度
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

# 顶帽
tophat = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, kernel)

# 黑帽
blackhat = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, kernel)

# 保存结果
cv2.imwrite(f'{OUTPUT_DIR}/morphology_opening.jpg', opening)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_closing.jpg', closing)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_gradient.jpg', gradient)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_tophat.jpg', tophat)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_blackhat.jpg', blackhat)

# 创建综合对比图
titles = ['Original', 'Opening', 'Closing', 'Gradient', 'Top Hat', 'Black Hat']
images = [binary, opening, closing, gradient, tophat, blackhat]
comparison = create_comparison(images, titles, 2, 3)
comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
cv2.imwrite(f'{OUTPUT_DIR}/morphology_all_operations.jpg', comparison)

print(f"  [OK] 组合操作完成")

# ==================== 3. 硬币计数 ====================
print("\n[3] 硬币计数项目...")

coins_path = get_image_path(COINS_PATH)
coins_img = imread_chinese(coins_path)

if coins_img is None:
    print("  [WARNING] 硬币图像读取失败，跳过硬币计数")
else:
    print(f"  [OK] 硬币图像读取成功: {coins_img.shape}")

    # 预处理
    gray = cv2.cvtColor(coins_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    binary_coins = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)

    # 形态学处理
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    closing_coins = cv2.morphologyEx(binary_coins, cv2.MORPH_CLOSE, kernel_close)
    final_coins = cv2.morphologyEx(closing_coins, cv2.MORPH_OPEN, kernel_open)

    cv2.imwrite(f'{OUTPUT_DIR}/coins_binary.jpg', binary_coins)
    cv2.imwrite(f'{OUTPUT_DIR}/coins_morphology.jpg', final_coins)

    # 查找轮廓
    contours, _ = cv2.findContours(final_coins, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 过滤小轮廓
    min_area = 100
    coins_contours = [c for c in contours if cv2.contourArea(c) > min_area]

    print(f"  检测到 {len(coins_contours)} 个硬币")

    # 标记硬币
    result = coins_img.copy()
    for i, contour in enumerate(coins_contours):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(result, f"#{i}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imwrite(f'{OUTPUT_DIR}/coins_result.jpg', result)

    print(f"  [OK] 硬币计数完成")

# ==================== 完成 ====================
print("\n" + "=" * 70)
print("所有操作完成！")
print(f"输出目录: {OUTPUT_DIR}/")
print("=" * 70)
```

---

## 🐛 调试技巧

### 常见错误及解决方法

#### 1. 形态学操作后图像全黑或全白
```python
# ❌ 错误：核太大或迭代次数太多
eroded = cv2.erode(binary, np.ones((20, 20), np.uint8), iterations=5)

# ✅ 正确：使用合适的核大小和迭代次数
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
eroded = cv2.erode(binary, kernel, iterations=1)
```

#### 2. 开运算和闭运算效果不明显
```python
# ❌ 错误：核大小不合适
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# ✅ 正确：根据噪声大小调整核
# 先观察噪声大小，然后选择核大小约为噪声的2倍
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
```

#### 3. 硬币计数不准确
```python
# ❌ 错误：直接查找轮廓不过滤
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# ✅ 正确：过滤小轮廓
min_area = 100  # 根据实际情况调整
coins = [c for c in contours if cv2.contourArea(c) > min_area]
```

#### 4. 形态学梯度边缘太粗
```python
# ❌ 错误：核太大
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

# ✅ 正确：使用小核
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
```

#### 5. 忘记二值化
```python
# ❌ 错误：直接对灰度图进行形态学操作
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
eroded = cv2.erode(gray, kernel)  # 结果不理想

# ✅ 正确：先二值化
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
eroded = cv2.erode(binary, kernel)
```

---

## ❓ 常见问题

### Q1: 如何选择合适的核大小？

**A:** 核大小的选择取决于应用场景：

```python
# 去除小的噪声点
noise_size = 3  # 假设噪声大小为3x3
kernel_size = noise_size * 2 - 1  # 核大小约为噪声的2倍
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 填充小的孔洞
hole_size = 5
kernel_size = hole_size * 2 - 1
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))

# 连接断裂的物体
gap_size = 7
kernel_size = gap_size * 2 - 1
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
```

**经验法则：**
- 小核（3x3）：轻微处理，保留细节
- 中核（5x5, 7x7）：常用，平衡效果和细节
- 大核（9x9以上）：强处理，可能损失细节

### Q2: 如何选择核的形状？

**A:** 不同形状有不同效果：

| 形状 | 效果 | 适用场景 |
|------|------|---------|
| MORPH_RECT | 最强，各向同性 | 通用，去噪、填充 |
| MORPH_ELLIPSE | 平滑，接近圆形 | 保留圆形特征 |
| MORPH_CROSS | 保留方向性 | 保留线条、十字形结构 |

```python
# 矩形核：最强效果
kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# [[1 1 1 1 1]
#  [1 1 1 1 1]
#  [1 1 1 1 1]
#  [1 1 1 1 1]
#  [1 1 1 1 1]]

# 椭圆形核：较平滑
kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
# [[0 0 1 0 0]
#  [0 1 1 1 0]
#  [1 1 1 1 1]
#  [0 1 1 1 0]
#  [0 0 1 0 0]]

# 十字形核：保留方向性
kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
# [[0 0 1 0 0]
#  [0 0 1 0 0]
#  [1 1 1 1 1]
#  [0 0 1 0 0]
#  [0 0 1 0 0]]
```

### Q3: 开运算和闭运算有什么区别？

**A:** 它们是相反的操作：

**开运算（先腐蚀后膨胀）：**
```python
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
# 等价于：
# temp = cv2.erode(binary, kernel)
# opening = cv2.dilate(temp, kernel)
```
- 去除小的白色区域
- 断开连接的物体
- 保持物体大致形状

**闭运算（先膨胀后腐蚀）：**
```python
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
# 等价于：
# temp = cv2.dilate(binary, kernel)
# closing = cv2.erode(temp, kernel)
```
- 填充小的黑色区域
- 连接断裂的物体
- 保持物体大致形状

**记忆技巧：**
- 开运算：打开（断开）物体，去除外来小白点
- 闭运算：闭合（连接）物体，填充内部小黑洞

### Q4: 形态学梯度、顶帽、黑帽有什么用？

**A:** 它们用于特定的提取任务：

**形态学梯度：**
```python
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
# 提取边缘（膨胀 - 腐蚀）
```
- 用途：边缘检测
- 优点：简单快速，边缘连续
- 缺点：边缘较粗，对噪声敏感

**顶帽变换：**
```python
tophat = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, kernel)
# 提取亮细节（原图 - 开运算）
```
- 用途：提取比周围区域亮的部分
- 应用：校正不均匀光照，提取小而亮的物体

**黑帽变换：**
```python
blackhat = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, kernel)
# 提取暗细节（闭运算 - 原图）
```
- 用途：提取比周围区域暗的部分
- 应用：检测裂缝、孔洞、暗区域

### Q5: 如何分离粘连的物体？

**A:** 使用分水岭算法或距离变换：

```python
def separate_touching_objects(image):
    """
    分离粘连的物体

    步骤:
    1. 距离变换
    2. 确定 markers
    3. 分水岭算法
    """
    # 1. 距离变换
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # 确保是二值图
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # 距离变换
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    cv2.imwrite('distance_transform.jpg', dist_transform)

    # 2. 确定前景（markers）
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max)
    sure_fg = np.uint8(sure_fg)

    # 确定背景
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # 未知区域
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 3. 标记 markers
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # 4. 分水岭算法
    if len(image.shape) == 3:
        img_color = image.copy()
    else:
        img_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    markers = cv2.watershed(img_color, markers)

    # 5. 可视化
    result = img_color.copy()
    result[markers == -1] = [0, 0, 255]  # 边界标记为红色

    return result, markers

# 使用
separated, markers = separate_touching_objects(binary)
cv2.imwrite('separated_objects.jpg', separated)
```

### Q6: 如何填充物体内部的孔洞？

**A:** 使用闭运算或轮廓填充：

```python
# 方法1：闭运算（简单）
def fill_holes_closing(binary):
    """使用闭运算填充孔洞"""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return closing

# 方法2：轮廓填充（精确）
def fill_holes_contour(binary):
    """使用轮廓填充孔洞"""
    # 复制图像
    filled = binary.copy()

    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 绘制轮廓（填充内部）
        cv2.drawContours(filled, [contour], 0, 255, -1)

    return filled

# 使用
filled_closing = fill_holes_closing(binary)
filled_contour = fill_holes_contour(binary)

cv2.imwrite('filled_closing.jpg', filled_closing)
cv2.imwrite('filled_contour.jpg', filled_contour)
```

### Q7: iterations 参数如何设置？

**A:** iterations 控制操作重复次数：

```python
# 单次操作
eroded_once = cv2.erode(binary, kernel, iterations=1)

# 多次操作（效果增强）
eroded_thrice = cv2.erode(binary, kernel, iterations=3)

# 迭代腐蚀（骨架化）
skeleton = binary.copy()
for i in range(10):
    skeleton = cv2.erode(skeleton, kernel, iterations=1)
    cv2.imwrite(f'skeleton_{i}.jpg', skeleton)
```

**效果：**
- iterations=1：标准效果
- iterations=2-3：增强效果
- iterations>3：强烈效果，可能过度

**建议：**
- 从 1 开始尝试
- 逐渐增加直到达到理想效果
- 不要一次性设置太大

### Q8: 如何加速形态学操作？

**A:** 优化方法：

```python
# 方法1：缩小图像
h, w = binary.shape
small = cv2.resize(binary, (w // 2, h // 2))
processed_small = cv2.morphologyEx(small, cv2.MORPH_OPEN, kernel)
processed = cv2.resize(processed_small, (w, h), interpolation=cv2.INTER_NEAREST)

# 方法2：使用更小的核
kernel_small = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
kernel_large = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
# 小核更快，大核更慢

# 方法3：减少操作次数
# ❌ 多次开运算
result = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)

# ✅ 使用更大的核代替
kernel_large = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
result = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_large)
```

### Q9: 形态学操作对彩色图像有效吗？

**A:** 形态学操作主要针对二值图或灰度图：

```python
# ❌ 错误：直接对彩色图操作
color_img = cv2.imread('image.jpg')
eroded = cv2.erode(color_img, kernel)  # 会对每个通道分别处理，效果不可预测

# ✅ 正确：先转灰度或二值
gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
eroded = cv2.erode(binary, kernel)

# 如果需要对彩色图操作，分别处理每个通道
b, g, r = cv2.split(color_img)
b_eroded = cv2.erode(b, kernel)
g_eroded = cv2.erode(g, kernel)
r_eroded = cv2.erode(r, kernel)
eroded_color = cv2.merge([b_eroded, g_eroded, r_eroded])
```

### Q10: 如何评估形态学处理效果？

**A:** 定量和定性结合：

```python
def evaluate_morphology(original, processed):
    """评估形态学处理效果"""

    # 1. 白色像素变化
    white_orig = np.count_nonzero(original)
    white_proc = np.count_nonzero(processed)
    change_ratio = (white_proc - white_orig) / white_orig

    # 2. 连通区域数量
    num_labels_orig, _ = cv2.connectedComponents(original)
    num_labels_proc, _ = cv2.connectedComponents(processed)

    # 3. 噪声估计（小连通域数量）
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    small_objects = sum(1 for c in contours if cv2.contourArea(c) < 100)

    return {
        'white_pixel_change': f"{change_ratio * 100:.1f}%",
        'num_components_orig': num_labels_orig,
        'num_components_proc': num_labels_proc,
        'small_objects': small_objects
    }

# 使用
metrics = evaluate_morphology(binary, opening)
print(f"白色像素变化: {metrics['white_pixel_change']}")
print(f"连通区域数: {metrics['num_components_orig']} -> {metrics['num_components_proc']}")
print(f"小对象数: {metrics['small_objects']}")
```

---

## 📚 参考资料

### 官方文档
- [OpenCV 形态学操作](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
- [cv2.erode 文档](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaeb1e0c1033e3f6b891a25d0511362aeb)
- [cv2.morphologyEx 文档](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga67493776e3ad1a3df638838393935e52)

### 项目文档
- [07-形态学操作](../../docs/07-形态学操作.md)
- [示例代码](../../src/examples/06-morphology.py)
- [工具函数](../../src/utils/)

### 扩展阅读
- [形态学图像处理](https://en.wikipedia.org/wiki/Mathematical_morphology)
- [分水岭算法](https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html)
- [距离变换](https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ga8a0b7fdfcb7441c0b3fba77ea9138138)

---

## 🎓 学习检查点

完成本任务后，你应该能够：
- [ ] 理解形态学操作的基本原理
- [ ] 掌握腐蚀和膨胀操作
- [ ] 理解开运算和闭运算的区别
- [ ] 掌握形态学梯度、顶帽、黑帽操作
- [ ] 根据场景选择合适的形态学操作
- [ ] 设计合适的结构元素（核大小和形状）
- [ ] 应用形态学操作去除噪声
- [ ] 应用形态学操作填充孔洞
- [ ] 应用形态学操作提取边缘
- [ ] 实现硬币计数等实际项目
- [ ] 评估和优化形态学处理效果

---

## 🚀 扩展挑战（可选）

完成基础任务后，可以尝试以下挑战：

### 挑战1：分水岭算法分离粘连物体

**目标：** 使用分水岭算法分离粘连在一起的硬币或细胞

**要求：**
- 实现距离变换
- 确定前景 markers
- 应用分水岭算法
- 可视化分割结果
- 处理不同粘连程度的情况

**代码框架：**
```python
def watershed_segmentation(binary):
    """使用分水岭算法分离粘连物体"""
    # 距离变换
    dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)

    # 确定 markers
    ret, fg = cv2.threshold(dist, 0.7 * dist.max)
    ret, markers = cv2.connectedComponents(np.uint8(fg))

    # 分水岭
    markers = cv2.watershed(img_color, markers)

    return markers
```

### 挑战2：骨架提取算法

**目标：** 实现图像的骨架提取

**要求：**
- 使用迭代腐蚀实现骨架化
- 保留物体的拓扑结构
- 可视化骨架化过程
- 对比不同算法的效果

**代码框架：**
```python
def skeletonize(binary):
    """骨架提取"""
    skeleton = np.zeros(binary.shape, np.uint8)

    while True:
        # 腐蚀
        eroded = cv2.erode(binary, kernel)

        # 开运算
        opened = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, kernel)

        # 提取骨架
        temp = cv2.subtract(eroded, opened)
        skeleton = cv2.bitwise_or(skeleton, temp)

        binary = eroded.copy()

        if cv2.countNonZero(binary) == 0:
            break

    return skeleton
```

### 挑战3：文本图像处理

**目标：** 处理扫描的文档图像

**要求：**
- 使用形态学操作去除文本噪声
- 填充字符内部孔洞
- 增强字符笔画
- 实现文本行的提取

### 挑战4：交互式形态学工具

**目标：** 实现实时调整形态学参数

**要求：**
- 使用 Trackbar 调整核大小
- 支持切换核形状
- 支持切换形态学操作类型
- 实时预览效果
- 显示操作时间和像素统计

### 挑战5：高级计数系统

**目标：** 实现通用的物体计数系统

**要求：**
- 支持不同大小的物体
- 处理部分遮挡的情况
- 统计物体的面积分布
- 生成详细的统计报告
- 可视化检测过程

---

**祝你好运！佛祖保佑，永无BUG！🙏**
