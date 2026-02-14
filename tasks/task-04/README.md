# Task 4: 图像阈值处理

## 📚 学习目标

通过完成本任务，你将掌握：
- ✅ 理解图像阈值分割的基本原理
- ✅ 掌握简单阈值处理的5种类型（BINARY、BINARY_INV、TRUNC、TOZERO、TOZERO_INV）
- ✅ 理解并实现 Otsu 自动阈值算法
- ✅ 掌握自适应阈值处理（均值、高斯）
- ✅ 学会根据场景选择合适的阈值方法
- ✅ 理解双峰直方图与 Otsu 方法的关系
- ✅ 实现交互式阈值调整工具
- ✅ 应用阈值处理解决实际问题（文档扫描、车牌识别等）
- ✅ 评估和优化阈值处理效果

## 🎯 任务概述

本任务要求你掌握图像阈值分割技术，这是图像处理中最重要的基础操作之一。阈值处理将灰度图像转换为二值图像，是许多高级视觉任务的预处理步骤。你将实现5种简单阈值、Otsu自动阈值和自适应阈值方法，并对比分析它们的优缺点和适用场景。

**预计时间：** 45-60 分钟
**难度：** ★★

## 📋 前置知识

在开始之前，确保你已经：
- [ ] 完成了 [Task 1: 图像基本操作](../task-01/README.md)
- [ ] 完成了 [Task 2: 色彩空间转换](../task-02/README.md)
- [ ] 阅读 [06-图像阈值处理](../../docs/06-图像阈值处理.md)
- [ ] 理解直方图的概念
- [ ] 理解什么是二值图像

## 🔧 开发环境

```bash
# 确保已安装必要的库
pip install opencv-python numpy matplotlib

# 测试图片位置
../../assets/sample-images/
```

**推荐测试图像：**
- `documents/text-document.jpg` - 文档图像（适合阈值处理）
- `basic/gradient.jpg` - 渐变图像（测试不同阈值类型）
- `basic/landscape.jpg` - 普通风景图
- 或自行拍摄包含明显明暗对比的图片

## 📝 任务要求

### 1. 简单阈值处理

**目标：** 掌握5种基本阈值类型的原理和效果

**要求：**
1. **实现5种阈值类型**
   - `cv2.THRESH_BINARY`：二值化
   - `cv2.THRESH_BINARY_INV`：反二值化
   - `cv2.THRESH_TRUNC`：截断
   - `cv2.THRESH_TOZERO`：低于阈值置0
   - `cv2.THRESH_TOZERO_INV`：高于阈值置0

2. **创建对比图**
   - 将所有5种阈值结果并排显示
   - 添加文字标签说明每种类型
   - 保存为 `threshold_types.jpg`

3. **理解每种类型的含义**
   - 编写注释说明每种阈值的效果
   - 分析适用场景

**核心代码：**
```python
import cv2
import numpy as np
import sys
import os

# 添加 utils 路径以支持中文路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

# 读取灰度图像
img_path = get_image_path('sample-images/basic/gradient.jpg')
img = imread_chinese(img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("错误：图像读取失败！")
    sys.exit(1)

# 设置阈值
thresh_value = 127
max_value = 255

# 1. THRESH_BINARY：二值化
#   像素值 > 阈值 → 设为 max_value (255)
#   像素值 ≤ 阈值 → 设为 0
ret, thresh1 = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_BINARY)

# 2. THRESH_BINARY_INV：反二值化
#   像素值 > 阈值 → 设为 0
#   像素值 ≤ 阈值 → 设为 max_value (255)
ret, thresh2 = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_BINARY_INV)

# 3. THRESH_TRUNC：截断
#   像素值 > 阈值 → 设为 阈值
#   像素值 ≤ 阈值 → 保持不变
ret, thresh3 = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_TRUNC)

# 4. THRESH_TOZERO：低于阈值置0
#   像素值 > 阈值 → 保持不变
#   像素值 ≤ 阈值 → 设为 0
ret, thresh4 = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_TOZERO)

# 5. THRESH_TOZERO_INV：高于阈值置0
#   像素值 > 阈值 → 设为 0
#   像素值 ≤ 阈值 → 保持不变
ret, thresh5 = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_TOZERO_INV)

# 打印结果信息
print(f"使用的阈值: {thresh_value}")
print(f"图像尺寸: {img.shape}")
print(f"像素范围: [{img.min)

# 保存所有结果
cv2.imwrite('threshold_binary.jpg', thresh1)
cv2.imwrite('threshold_binary_inv.jpg', thresh2)
cv2.imwrite('threshold_trunc.jpg', thresh3)
cv2.imwrite('threshold_tozero.jpg', thresh4)
cv2.imwrite('threshold_tozero_inv.jpg', thresh5)

# 创建对比图（3行2列）
titles = ['Original', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

# 为每个图像添加文字标签
for i in range(6):
    if i == 0:  # 原图
        img_labeled = cv2.cvtColor(images[i], cv2.COLOR_GRAY2BGR)
    else:
        img_labeled = cv2.cvtColor(images[i], cv2.COLOR_GRAY2BGR)

    cv2.putText(img_labeled, titles[i], (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    images[i] = img_labeled

# 组合图像
row1 = np.hstack([images[0], images[1], images[2]])
row2 = np.hstack([images[3], images[4], images[5]])
comparison = np.vstack([row1, row2])

# 保存对比图
cv2.imwrite('threshold_types.jpg', comparison)
print("所有阈值类型已保存到 threshold_types.jpg")
```

**5种阈值类型详解：**

| 类型 | 效果描述 | 适用场景 | 效果 |
|------|---------|---------|------|
| **BINARY** | >阈值→255, ≤阈值→0 |
| **BINARY_INV** | >阈值→0, ≤阈值→255 | 提取暗色物体 | 与BINARY相反 |
| **TRUNC** | >阈值→阈值, ≤阈值不变 | 调整亮度、去除高光 | 保留暗部细节，压缩亮部 |
| **TOZERO** | >阈值不变, ≤阈值→0 | 去除暗背景，保留亮物体 | 只保留亮部区域 |
| **TOZERO_INV** | >阈值→0, ≤阈值不变 | 去除亮背景，保留暗物体 | 只保留暗部区域 |

**提示：**
- 所有阈值操作都需要灰度图像
- 阈值选择很重要，可以通过直方图分析确定
- BINARY 和 BINARY_INV 产生真正的二值图像（只有0和255）
- TRUNC、TOZERO、TOZERO_INV 保留部分灰度信息

---

### 2. Otsu 自动阈值

**目标：** 理解 Otsu 算法原理，实现自动阈值选择

**要求：**
1. **实现 Otsu 阈值**
   - 使用 `cv2.THRESH_OTSU` 标志
   - 打印自动计算的最佳阈值
   - 保存结果为 `threshold_otsu.jpg`

2. **对比固定阈值**
   - 使用固定阈值127
   - 对比 Otsu 和固定阈值的效果
   - 创建对比图并保存

3. **绘制直方图**
   - 绘制图像直方图
   - 在直方图上标记 Otsu 阈值位置
   - 分析双峰特性
   - 保存为 `histogram_otsu.jpg`

**完整代码框架：**
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取灰度图像
img = cv2.imread('text-document.jpg', cv2.IMREAD_GRAYSCALE)

# 方法1：固定阈值（手动设置为127）
ret1, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
print(f"固定阈值: 127")

# 方法2：Otsu 自动阈值
# 注意：阈值参数设为0，并添加 cv2.THRESH_OTSU 标志
ret2, thresh2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(f"Otsu 自动计算的阈值: {ret2}")

# 保存结果
cv2.imwrite('threshold_manual.jpg', thresh1)
cv2.imwrite('threshold_otsu.jpg', thresh2)

# 创建对比图
comparison = np.hstack([img, thresh1, thresh2])
cv2.imwrite('threshold_comparison.jpg', comparison)

# 绘制直方图
plt.figure(figsize=(10, 6))
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.plot(hist, color='b')
plt.axvline(x=ret2, color='r', linestyle='--', linewidth=2, label=f'Otsu Threshold = {ret2:.2f}')
plt.axvline(x=127, color='g', linestyle='--', linewidth=2, label='Manual Threshold = 127')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.title('Image Histogram with Thresholds')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('histogram_otsu.jpg', dpi=150, bbox_inches='tight')
plt.close()

print("固定阈值图像: threshold_manual.jpg")
print("Otsu阈值图像: threshold_otsu.jpg")
print("对比图: threshold_comparison.jpg")
print("直方图: histogram_otsu.jpg")
```

**Otsu 算法原理：**

Otsu 方法通过最大化类间方差来寻找最佳阈值：

```
类间方差 = ω₀ × ω₁ × (μ₀ - μ₁)²

其中：
- ω₀：前景像素占比
- ω₁：背景像素占比
- μ₀：前景平均灰度
- μ₁：背景平均灰度
```

**Otsu 适用条件：**
- ✅ 图像直方图呈现**双峰**分布
- ✅ 前景和背景灰度值有明显差异
- ✅ 光照相对均匀
- ❌ 不适合单峰或多峰直方图
- ❌ 不适合光照不均的图像

**判断是否适合 Otsu：**
```python
def is_suitable_for_otsu(img):
    """
    判断图像是否适合 Otsu 阈值

    通过分析直方图判断是否有明显的双峰
    """
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist = hist.flatten()

    # 找峰值
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(hist, distance=30, prominence=100)

    if len(peaks) >= 2:
        print(f"检测到 {len(peaks)} 个峰值，适合 Otsu")
        return True
    else:
        print(f"检测到 {len(peaks)} 个峰值，可能不适合 Otsu")
        return False

# 使用
if is_suitable_for_otsu(img):
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
else:
    print("建议使用自适应阈值")
```

**提示：**
- 使用 Otsu 时，阈值参数必须设为 0
- 返回值 ret 是 Otsu 计算的最佳阈值
- 打印阈值值有助于理解算法结果
- 对比固定阈值和 Otsu 效果可以看出优势

---

### 3. 自适应阈值处理

**目标：** 掌握自适应阈值方法，处理光照不均的图像

**要求：**
1. **实现两种自适应方法**
   - `cv2.ADAPTIVE_THRESH_MEAN_C`：邻域均值
   - `cv2.ADAPTIVE_THRESH_GAUSSIAN_C`：邻域高斯加权

2. **参数调优实验**
   - 尝试不同的 blockSize（7, 11, 15）
   - 尝试不同的 C 值（2, 5, 10）
   - 记录最佳参数组合
   - 保存结果为 `threshold_adaptive_best.jpg`

3. **创建对比图**
   - 对比固定阈值、Otsu、自适应均值、自适应高斯
   - 保存为 `threshold_all_comparison.jpg`
   - 分析各方法在不同场景的效果

**完整代码框架：**
```python
import cv2
import numpy as np

# 读取灰度图像（最好是光照不均的图像）
img = cv2.imread('uneven-lighting.jpg', cv2.IMREAD_GRAYSCALE)

# 1. 全局固定阈值
ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# 2. Otsu 阈值
ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 3. 自适应阈值 - 均值法
# blockSize: 邻域大小（必须是奇数）
# C: 从均值减去的常数
th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY, 11, 2)

# 4. 自适应阈值 - 高斯法
th4 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY, 11, 2)

# 保存结果
cv2.imwrite('threshold_global.jpg', th1)
cv2.imwrite('threshold_otsu.jpg', th2)
cv2.imwrite('threshold_adaptive_mean.jpg', th3)
cv2.imwrite('threshold_adaptive_gaussian.jpg', th4)

# 创建对比图（2行3列）
# 为每个图像添加标题
def add_title(image, title):
    """在图像上添加标题"""
    img_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.putText(img_bgr, title, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return img_bgr

titles = ['Original', 'Global (127)', 'Otsu', 'Adaptive Mean', 'Adaptive Gaussian', 'Best Result']
images = [img, th1, th2, th3, th4, th4]

labeled_images = []
for i in range(6):
    labeled = add_title(images[i], titles[i])
    labeled_images.append(labeled)

# 组合图像
row1 = np.hstack(labeled_images[:3])
row2 = np.hstack(labeled_images[3:])
comparison = np.vstack([row1, row2])

# 缩放到合适大小
comparison = cv2.resize(comparison, None, fx=0.6, fy=0.6)
cv2.imwrite('threshold_all_comparison.jpg', comparison)

print(f"全局阈值 (127): threshold_global.jpg")
print(f"Otsu 阈值 ({ret2}): threshold_otsu.jpg")
print(f"自适应均值: threshold_adaptive_mean.jpg")
print(f"自适应高斯: threshold_adaptive_gaussian.jpg")
print(f"对比图: threshold_all_comparison.jpg")

# ==================== 参数调优 ====================
print("\n参数调优实验...")

best_score = 0
best_params = None

# 尝试不同的参数组合
for blockSize in [7, 9, 11, 13, 15]:
    for C in [2, 3, 5, 7, 10]:
        # 自适应高斯
        thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, blockSize, C)

# 光照不均匀严重
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 15, 5)

# 图像细节多，需要保留
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 7, 2)

# 噪声较多的图像
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 15, 10)
```

**自适应 vs 全局阈值：**

| 特性 | 全局阈值 | Otsu | 自适应均值 | 自适应高斯 |
|------|---------|------|-----------|-----------|
| **光照均匀** | ✅ 优秀 | ✅ 优秀 | ✅ 良好 | ✅ 良好 |
| **光照不均** | ❌ 差 | ❌ 差 | ✅ 良好 | ✅ 优秀 |
| **计算速度** | ★★★★★ | ★★★★ | ★★★ | ★★ |
| **参数调节** | 阈值 | 无 | blockSize, C | blockSize, C |
| **适用场景** | 光照均匀 | 双峰直方图 | 光照不均 | 光照不均（推荐） |

**提示：**
- blockSize 必须是奇数（3, 5, 7, 9, 11, ...）
- blockSize 越大，计算越慢，但效果越平滑
- C 值用于微调，通常取 2-10
- 优先使用 GAUSSIAN_C 方法，效果更好
- 自适应阈值不适合用于非常小的图像（< 100x100）

---

### 4. 实际应用：文档扫描预处理

**目标：** 将阈值处理应用到实际问题，实现文档扫描预处理流程

**要求：**
1. **实现完整的预处理流程**
   - 读取彩色文档图像
   - 转换为灰度图
   - 高斯滤波降噪
   - 自适应阈值二值化
   - 形态学操作去除噪声
   - 保存最终结果

2. **对比不同流程**
   - 方案1：直接阈值
   - 方案2：滤波 + 阈值
   - 方案3：滤波 + 阈值 + 形态学
   - 分析每一步的作用

3. **评估处理效果**
   - 计算前景像素占比
   - 统计噪声点数量
   - 生成处理报告

**完整代码框架：**
```python
import cv2
import numpy as np

def preprocess_document(image_path, output_path):
    """
    文档图像预处理流程

    参数:
        image_path: 输入图像路径
        output_path: 输出图像路径
    """
    # 1. 读取图像
    img = cv2.imread(image_path)
    if img is None:
        print(f"错误：无法读取图像 {image_path}")
        return None

    print(f"原始图像尺寸: {img.shape}")

    # 2. 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"[1] 灰度转换完成")

    # 3. 高斯滤波降噪
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    print(f"[2] 高斯滤波完成")

    # 4. 自适应阈值
    binary = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )
    print(f"[3] 自适应阈值完成")

    # 5. 形态学操作去除噪声
    kernel = np.ones((2, 2), np.uint8)

    # 开运算：去除小的白色噪声
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    print(f"[4] 形态学开运算完成")

    # 闭运算：填充小的黑色空洞
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    print(f"[5] 形态学闭运算完成")

    # 保存结果
    cv2.imwrite(output_path, closed)
    print(f"[6] 结果已保存到 {output_path}")

    # 统计信息
    total_pixels = closed.size
    foreground_pixels = np.count_nonzero(closed)
    foreground_ratio = (foreground_pixels / total_pixels) * 100

    print(f"\n处理结果统计:")
    print(f"  - 总像素数: {total_pixels}")
    print(f"  - 前景像素: {foreground_pixels} ({foreground_ratio:.2f}%)")
    print(f"  - 背景像素: {total_pixels - foreground_pixels} ({100-foreground_ratio:.2f}%)")

    return closed

# 使用示例
if __name__ == "__main__":
    input_path = 'document.jpg'
    output_path = 'document_processed.jpg'

    result = preprocess_document(input_path, output_path)

    if result is not None:
        print("\n处理完成！")
```

**创建对比图：**
```python
import cv2
import numpy as np

img = cv2.imread('document.jpg')

# 不同处理方案
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 方案1：直接阈值（不推荐）
ret1, th1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 方案2：滤波 + 阈值
blur = cv2.GaussianBlur(gray, (5, 5), 0)
ret2, th2 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 方案3：滤波 + 自适应阈值
th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY, 11, 2)

# 方案4：完整流程（推荐）
kernel = np.ones((2, 2), np.uint8)
opened = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel)
th4 = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

# 创建对比图
titles = ['Original', 'Direct Threshold', 'Blur+Otsu', 'Adaptive', 'With Morphology', 'Final Result']
images = [img, th1, th2, th3, th4, th4]

# 转换为彩色并添加标签
labeled_images = []
for i in range(6):
    if len(images[i].shape) == 2:
        img_labeled = cv2.cvtColor(images[i], cv2.COLOR_GRAY2BGR)
    else:
        img_labeled = images[i].copy()

    cv2.putText(img_labeled, titles[i], (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    labeled_images.append(img_labeled)

# 组合（2行3列）
row1 = np.hstack(labeled_images[:3])
row2 = np.hstack(labeled_images[3:])
comparison = np.vstack([row1, row2])
comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
cv2.imwrite('document_preprocess_comparison.jpg', comparison)
print("文档预处理对比图已保存")
```

**提示：**
- 文档扫描预处理的关键是自适应阈值
- 形态学操作可以去除扫描产生的噪声
- 高斯滤波有助于平滑纸张纹理
- blockSize 和 C 参数需要根据文档调整

---

## 📦 提交要求

### 必交内容

1. **代码文件**：`task4_solution.py`
   - 包含所有4个任务的实现
   - 代码注释清晰，符合 PEP 8 规范
   - 包含交互式阈值调整功能（）

2. **保存的图像**（按任务要求命名）：
   ```
   threshold_types.jpg              # 5种阈值类型对比
   threshold_comparison.jpg         # 固定阈值 vs Otsu
   histogram_otsu.jpg               # 直方图 + Otsu阈值
   threshold_all_comparison.jpg     # 所有方法对比
   threshold_adaptive_best.jpg      # 最佳自适应阈值结果
   document_processed.jpg           # 文档预处理结果（选做）
   document_preprocess_comparison.jpg # 文档处理对比（选做）
   ```

3. **处理报告**：`threshold_analysis_report.txt` 或 `report.md`
   - 对比5种阈值类型的特点和适用场景
   - 分析固定阈值、Otsu、自适应阈值的优缺点
   - 总结参数调优经验
   - 至少 400 字

4. **运行结果截图**：`result_screenshot.png`
   - 显示程序运行的控制台输出
   - 包含处理参数和统计信息

### 提交格式

```
task-04-submission/
├── task4_solution.py               # 你的代码
├── result_screenshot.png           # 运行结果截图
├── threshold_analysis_report.txt   # 分析报告
├── output_images/                  # 输出图像文件夹
│   ├── threshold_types.jpg
│   ├── threshold_binary.jpg
│   ├── threshold_binary_inv.jpg
│   ├── threshold_trunc.jpg
│   ├── threshold_tozero.jpg
│   ├── threshold_tozero_inv.jpg
│   ├── threshold_otsu.jpg
│   ├── histogram_otsu.jpg
│   ├── threshold_adaptive_mean.jpg
│   ├── threshold_adaptive_gaussian.jpg
│   ├── threshold_all_comparison.jpg
│   └── threshold_adaptive_best.jpg
└── report.md                       # 实验报告（可选）
```

---

## 💡 完整代码框架

```python
"""
Task 4: 图像阈值处理
姓名：[你的名字]
学号：[你的学号]
日期：[提交日期]
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# ==================== 配置区 ====================
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

# 图片路径
IMG_PATH = 'sample-images/basic/gradient.jpg'
DOC_PATH = 'sample-images/documents/text-document.jpg'
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

def create_labeled_grid(images, titles, rows, cols):
    """创建带标签的图像网格"""
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
print("Task 4: 图像阈值处理")
print("=" * 70)

# ==================== 1. 简单阈值处理 ====================
print("\n[1] 简单阈值处理（5种类型）...")

img_path = get_image_path(IMG_PATH)
img = imread_chinese(img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("  [ERROR] 图像读取失败！")
    sys.exit(1)

print(f"  [OK] 图像读取成功: {img.shape}")
print(f"  - 像素范围: [{img.min)

# 设置阈值参数
thresh_value = 127
max_value = 255

# 应用5种阈值类型
ret, thresh_binary = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_BINARY)
ret, thresh_binary_inv = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_BINARY_INV)
ret, thresh_trunc = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_TRUNC)
ret, thresh_tozero = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_TOZERO)
ret, thresh_tozero_inv = cv2.threshold(img, thresh_value, max_value, cv2.THRESH_TOZERO_INV)

# 保存结果
cv2.imwrite(f'{OUTPUT_DIR}/threshold_binary.jpg', thresh_binary)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_binary_inv.jpg', thresh_binary_inv)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_trunc.jpg', thresh_trunc)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_tozero.jpg', thresh_tozero)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_tozero_inv.jpg', thresh_tozero_inv)

# 创建对比图
titles = ['Original', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh_binary, thresh_binary_inv, thresh_trunc, thresh_tozero, thresh_tozero_inv]
comparison = create_labeled_grid(images, titles, 2, 3)
comparison = cv2.resize(comparison, None, fx=0.6, fy=0.6)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_types.jpg', comparison)

print(f"  [OK] 所有阈值类型已保存")
print(f"  - 使用的阈值: {thresh_value}")

# 打印各类型的像素统计
print(f"\n  像素统计（前景像素占比）:")
for name, result in zip(titles[1:], images[1:]):
    foreground_ratio = (np.count_nonzero(result) / result.size) * 100
    print(f"  - {name:<15}: {foreground_ratio:6.2f}%")

# ==================== 2. Otsu 自动阈值 ====================
print("\n[2] Otsu 自动阈值...")

# 固定阈值
ret_manual, thresh_manual = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
print(f"  固定阈值: 127")

# Otsu 自动阈值
ret_otsu, thresh_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(f"  Otsu 阈值: {ret_otsu:.2f}")

# 保存结果
cv2.imwrite(f'{OUTPUT_DIR}/threshold_manual.jpg', thresh_manual)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_otsu.jpg', thresh_otsu)

# 创建对比图
titles = ['Original', 'Manual (127)', f'Otsu ({ret_otsu:.1f})']
images = [img, thresh_manual, thresh_otsu]
comparison = create_labeled_grid(images, titles, 1, 3)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_comparison.jpg', comparison)

# 绘制直方图
plt.figure(figsize=(10, 6))
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.plot(hist, color='b', linewidth=1)
plt.axvline(x=ret_otsu, color='r', linestyle='--', linewidth=2, label=f'Otsu Threshold = {ret_otsu:.2f}')
plt.axvline(x=127, color='g', linestyle='--', linewidth=2, label='Manual Threshold = 127')
plt.xlabel('Pixel Value', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Image Histogram with Thresholds', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/histogram_otsu.jpg', dpi=150)
plt.close()

print(f"  [OK] Otsu 阈值处理完成")
print(f"  - 直方图已保存")

# ==================== 3. 自适应阈值 ====================
print("\n[3] 自适应阈值处理...")

# 读取文档图像（更适合自适应阈值）
doc_path = get_image_path(DOC_PATH)
doc_img = imread_chinese(doc_path, cv2.IMREAD_GRAYSCALE)

if doc_img is None:
    print("  [WARNING] 文档图像读取失败，使用原图")
    doc_img = img

# 全局阈值
ret_global, thresh_global = cv2.threshold(doc_img, 127, 255, cv2.THRESH_BINARY)

# Otsu 阈值
ret_otsu_doc, thresh_otsu_doc = cv2.threshold(doc_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 自适应均值
thresh_mean = cv2.adaptiveThreshold(doc_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 11, 2)

# 自适应高斯
thresh_gaussian = cv2.adaptiveThreshold(doc_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)

# 保存结果
cv2.imwrite(f'{OUTPUT_DIR}/threshold_global.jpg', thresh_global)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_otsu_doc.jpg', thresh_otsu_doc)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_adaptive_mean.jpg', thresh_mean)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_adaptive_gaussian.jpg', thresh_gaussian)

# 创建对比图
titles = ['Original', 'Global (127)', f'Otsu ({ret_otsu_doc:.1f})',
          'Adaptive Mean', 'Adaptive Gaussian', 'Best']
images = [doc_img, thresh_global, thresh_otsu_doc, thresh_mean, thresh_gaussian, thresh_gaussian]
comparison = create_labeled_grid(images, titles, 2, 3)
comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
cv2.imwrite(f'{OUTPUT_DIR}/threshold_all_comparison.jpg', comparison)

print(f"  [OK] 自适应阈值处理完成")

# 参数调优
print(f"\n  参数调优实验...")
best_score = 0
best_params = None

for blockSize in [7, 9, 11, 13, 15]:
    for C in [2, 3, 5, 7, 10]:
        thresh = cv2.adaptiveThreshold(doc_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, blockSize, C)

# ==================== 4. 文档预处理（可选）====================
print("\n[4] 文档预处理应用（可选）...")

if doc_img is not None:
    # 完整预处理流程
    blurred = cv2.GaussianBlur(doc_img, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # 形态学操作
    kernel = np.ones((2, 2), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    final = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite(f'{OUTPUT_DIR}/document_processed.jpg', final)

    # 统计
    foreground_ratio = (np.count_nonzero(final) / final.size) * 100
    print(f"  [OK] 文档预处理完成")
    print(f"  - 前景像素占比: {foreground_ratio:.2f}%")

# ==================== 生成报告 ====================
print("\n[5] 生成分析报告...")

report = f"""
# 图像阈值处理分析报告

## 1. 简单阈值类型对比

### 5种阈值类型特点：

| 类型 | 效果 | 适用场景 | 前景占比 |
|------|------|---------|---------|
| BINARY | >127→255, ≤127→0 |
| BINARY_INV | >127→0, ≤127→255 | 提取暗色物体 | {np.count_nonzero(thresh_binary_inv)/thresh_binary_inv.size*100:.2f}% |
| TRUNC | >127→127, ≤127不变 | 调整亮度、去除高光 | {np.count_nonzero(thresh_trunc)/thresh_trunc.size*100:.2f}% |
| TOZERO | >127不变, ≤127→0 | 去除暗背景 | {np.count_nonzero(thresh_tozero)/thresh_tozero.size*100:.2f}% |
| TOZERO_INV | >127→0, ≤127不变 | 去除亮背景 | {np.count_nonzero(thresh_tozero_inv)/thresh_tozero_inv.size*100:.2f}% |

## 2. 固定阈值 vs Otsu

- 固定阈值: 127
- Otsu阈值: {ret_otsu:.2f}
- 差异: {abs(ret_otsu - 127):.2f}

**Otsu 优势：**
- 自动计算最佳阈值
- 适合双峰直方图图像
- 无需手动调参

**Otsu 限制：**
- 仅适合光照均匀的图像
- 需要明显的双峰直方图
- 不适合复杂场景

## 3. 自适应阈值分析

### 全局阈值 vs 自适应阈值：

| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| 全局阈值 | 快速简单 | 光照不均效果差 | 光照均匀 |
| Otsu | 自动阈值 |
| 自适应均值 | 处理光照不均 | 计算较慢 | 光照不均 |
| 自适应高斯 | 效果最好 | 计算最慢 | 光照不均（推荐） |

### 最佳参数：
- blockSize: {best_params[0]}
- C: {best_params[1]}

## 4. 实际应用建议

### 文档扫描：
1. 转灰度
2. 高斯滤波 (5x5)
3. 自适应阈值 (GAUSSIAN_C, blockSize=11, C=2)
4. 形态学去噪 (2x2 kernel)

### 车牌识别：
1. 转灰度
2. 高斯滤波
3. Sobel 边缘检测
4. Otsu 阈值

### 物体分割：
- 光照均匀: 全局阈值或 Otsu
- 光照不均: 自适应阈值 (GAUSSIAN_C)

## 5. 总结

阈值处理是图像分割的基础技术，选择合适的方法至关重要：
- **简单场景**: 全局阈值
- **双峰分布**: Otsu
- **光照不均**: 自适应阈值（推荐 GAUSSIAN_C）

关键在于理解每种方法的原理和适用场景，根据实际问题选择最合适的方案。
"""

with open(f'{OUTPUT_DIR}/threshold_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"  [OK] 分析报告已保存")

# ==================== 完成 ====================
print("\n" + "=" * 70)
print("所有操作完成！")
print(f"输出目录: {OUTPUT_DIR}/")
print("=" * 70)
```

---

## 🐛 调试技巧

### 常见错误及解决方法

#### 1. 阈值处理后的图像全黑或全白
```python
# ❌ 错误：阈值设置不当
ret, thresh = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)  # 阈值太高

# ✅ 正确：先分析直方图确定阈值
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
# 找到波谷位置作为阈值
# 或者使用 Otsu
ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

#### 2. 自适应阈值效果很差
```python
# ❌ 错误：参数设置不当
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 3, 50)  # blockSize 太小，C 太大

# ✅ 正确：使用合理的参数
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 11, 2)  # 推荐初始值
```

#### 3. Otsu 效果不理想
```python
# ❌ 错误：直接使用 Otsu 而不检查直方图
ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# ✅ 正确：先检查直方图是否适合 Otsu
def check_histogram_peaks(img):
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # 简单判断：是否有明显的双峰
    # 可以用 find_peaks 或其他方法
    return has_two_peaks

if check_histogram_peaks(img):
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
else:
    print("不适合 Otsu，使用自适应阈值")
    thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
```

#### 4. 忘记转换为灰度图
```python
# ❌ 错误：直接对彩色图像进行阈值处理
img = cv2.imread('image.jpg')
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)  # 错误！

# ✅ 正确：先转灰度
img = cv2.imread('image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # 正确
```

#### 5. blockSize 不是奇数
```python
# ❌ 错误：blockSize 是偶数
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 10, 2)  # blockSize=10 错误

# ✅ 正确：blockSize 必须是奇数
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 11, 2)  # blockSize=11 正确
```

---

## ❓ 常见问题

### Q1: 如何选择合适的阈值？

**A:** 有多种方法：

**方法1：手动选择（通过直方图）**
```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# 绘制直方图
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.plot(hist)
plt.axvline(x=127, color='r', linestyle='--')
plt.show()

# 找到波谷位置作为阈值
```

**方法2：Otsu 自动计算**
```python
ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(f"Otsu 计算的阈值: {ret}")
```

**方法3：自适应阈值（光照不均）**
```python
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 11, 2)
```

**方法4：迭代法**
```python
def iterative_threshold(img, epsilon=0.5):
    """迭代法寻找最佳阈值"""
    threshold = np.mean(img)
    while True:
        # 根据当前阈值分割前景和背景
        foreground = img[img > threshold].mean()
        background = img[img <= threshold].mean()
        new_threshold = (foreground + background) / 2

        if abs(new_threshold - threshold) < epsilon:
            break
        threshold = new_threshold

    return threshold

best_thresh = iterative_threshold(img)
print(f"迭代法阈值: {best_thresh}")
```

### Q2: 二值化的实际应用场景有哪些？

**A:** 常见应用包括：

**1. 文档扫描和 OCR 预处理**
```python
# 文档二值化是 OCR 的必要步骤
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)
```

**2. 车牌定位**
```python
# 车牌区域通常是高对比度区域
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobelx = np.uint8(np.absolute(sobelx))
ret, thresh = cv2.threshold(sobelx, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

**3. 物体分割和计数**
```python
# 分割前景物体进行计数
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"检测到 {len(contours)} 个物体")
```

**4. 图像压缩**
```python
# 二值图像只有 0 和 255，可以大幅压缩
ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
cv2.imwrite('compressed.png', binary, [cv2.IMWRITE_PNG_BILEVEL, 1])
```

**5. 条形码和二维码识别**
```python
# 条形码需要高对比度的二值图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

### Q3: 为什么自适应阈值 blockSize 必须是奇数？

**A:** 因为自适应阈值需要中心像素周围对称的邻域：

```
如果 blockSize = 3 (奇数):
  [x x x]
  [x c x]  c 是中心像素，周围对称
  [x x x]

如果 blockSize = 4 (偶数):
  [x x x x]
  [x x c x]  c 无法居中，不对称
  [x x x x]
```

奇数保证了有一个明确的中心像素，邻域对称分布。

### Q4: 如何处理光照严重不均的图像？

**A:** 有多种方法：

**方法1：自适应阈值（推荐）**
```python
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, 15, 5)
# 使用较大的 blockSize 和 C
```

**方法2：局部对比度归一化**
```python
def local_normalize(img, kernel_size=(15, 15)):
    """局部对比度归一化"""
    blur = cv2.GaussianBlur(img, kernel_size, 0)
    num = img.astype(float) - blur
    denom = np.std(img) + 1e-6
    normalized = num / denom
    normalized = np.uint8((normalized + 2) * 40)
    return np.clip(normalized, 0, 255)

normalized = local_normalize(gray)
ret, thresh = cv2.threshold(normalized, 127, 255, cv2.THRESH_BINARY)
```

**方法3：形态学顶帽变换**
```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (51, 51))
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
ret, thresh = cv2.threshold(tophat, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

### Q5: 如何评估阈值处理的效果？

**A:** 定量和定性结合：

**定量评估：**
```python
def evaluate_threshold(thresh_img):
    """评估阈值处理效果"""
    total = thresh_img.size
    foreground = np.count_nonzero(thresh_img)
    background = total - foreground

    # 1. 前景占比（理想情况 30-50%）
    fg_ratio = (foreground / total) * 100

    # 2. 噪声估计（小于某个阈值的小连通域数量）
    num_labels, labels = cv2.connectedComponents(thresh_img)

    # 3. 连通性分析
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    num_objects = len(contours)

    return {
        'foreground_ratio': fg_ratio,
        'num_components': num_labels,
        'num_objects': num_objects
    }

metrics = evaluate_threshold(thresh)
print(f"前景占比: {metrics['foreground_ratio']:.2f}%")
print(f"连通区域数: {metrics['num_components']}")
print(f"物体数量: {metrics['num_objects']}")
```

**定性评估：**
- 目视检查：文本是否清晰
- 边缘完整性：物体边缘是否连续
- 噪声程度：是否有孤立的小噪点
- 细节保留：重要信息是否丢失

### Q6: TRUNC、TOZERO 等阈值类型有什么用？

**A:** 它们用于特定场景：

**TRUNC（截断）：**
```python
# 用途：去除高光，保留暗部细节
ret, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_TRUNC)
# 大于200的像素被设为200，其他不变
# 适合：去除镜面反射、过曝区域
```

**TOZERO（低于阈值置0）：**
```python
# 用途：去除暗背景，只保留亮物体
ret, thresh = cv2.threshold(img, 100, 255, cv2.THRESH_TOZERO)
# 小于等于100的置0，大于100的保持原值
# 适合：提取亮色物体、去除黑色背景
```

**TOZERO_INV（高于阈值置0）：**
```python
# 用途：去除亮背景，只保留暗物体
ret, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_TOZERO_INV)
# 大于150的置0，小于等于150的保持原值
# 适合：提取暗色文字、去除白色背景
```

### Q7: 如何实现多阈值分割？

**A:** 将灰度级分为多个区间：

```python
def multi_threshold(img, thresholds):
    """
    多阈值分割

    参数:
        img: 灰度图像
        thresholds: 阈值列表，如 [80, 150, 220]

    返回:
        分割后的图像（不同区域用不同灰度值表示）
    """
    result = np.zeros_like(img)

    # 第一个区间：[0, thresholds[0]]
    result[img <= thresholds[0]] = 50

    # 中间区间
    for i in range(len(thresholds) - 1):
        mask = (img > thresholds[i]) & (img <= thresholds[i + 1])
        result[mask] = 50 + (i + 1) * (200 // len(thresholds))

    # 最后一个区间：(thresholds[-1], 255]
    result[img > thresholds[-1]] = 255

    return result

# 使用
img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
multi_thresh = multi_threshold(img, [80, 150, 220])
cv2.imwrite('multi_threshold.jpg', multi_thresh)
```

### Q8: Otsu 在什么情况下会失败？

**A:** 以下情况 Otsu 效果差：

**1. 单峰直方图**
```python
# 直方图只有一个峰，Otsu 找不到合适的分割点
# 解决：使用全局固定阈值或自适应阈值
```

**2. 多峰直方图**
```python
# 直方图有多个峰（前景有多个灰度级）
# 解决：多阈值分割或聚类算法
```

**3. 光照不均**
```python
# 不同区域亮度差异大
# 解决：自适应阈值
```

**4. 前景和背景比例严重失调**
```python
# 前景只占 1-5%，背景占 95-99%
# 解决：调整区域权重或使用自适应阈值
```

### Q9: 如何加速自适应阈值处理？

**A:** 优化方法：

**方法1：缩小图像**
```python
h, w = img.shape
small = cv2.resize(img, (w // 2, h // 2))
thresh_small = cv2.adaptiveThreshold(small, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)
thresh = cv2.resize(thresh_small, (w, h), interpolation=cv2.INTER_NEAREST)
```

**方法2：使用均值代替高斯**
```python
# MEAN_C 比 GAUSSIAN_C 快约 3-5 倍
thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY, 11, 2)
```

**方法3：使用更小的 blockSize**
```python
# blockSize=7 比 blockSize=15 快
thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 7, 2)
```

---

## 📚 参考资料

### 官方文档
- [OpenCV 图像阈值处理](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
- [cv2.threshold 文档](https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199c9b9c)
- [cv2.adaptiveThreshold 文档](https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ga72b913f352e67a6de23a59852d26a184)

### 项目文档
- [06-图像阈值处理](../../docs/06-图像阈值处理.md)
- [示例代码](../../src/examples/05-thresholding.py)
- [工具函数](../../src/utils/)

### 扩展阅读
- [Otsu 方法原理论文](https://ieeexplore.ieee.org/document/4310076)
- [自适应阈值详解](https://homepages.inf.ed.ac.uk/rbf/HIPR2/adpthrsh.htm)
- [图像分割算法综述](https://en.wikipedia.org/wiki/Thresholding_(image_processing))

---

## 🎓 学习检查点

完成本任务后，你应该能够：
- [ ] 理解图像阈值分割的基本原理
- [ ] 掌握5种简单阈值类型的效果和用途
- [ ] 熟练使用 `cv2.threshold()` 进行固定阈值处理
- [ ] 理解 Otsu 算法的原理和适用条件
- [ ] 掌握 `cv2.adaptiveThreshold()` 进行自适应阈值处理
- [ ] 区分 MEAN_C 和 GAUSSIAN_C 的差异
- [ ] 根据图像特性选择合适的阈值方法
- [ ] 调优自适应阈值的 blockSize 和 C 参数
- [ ] 实现文档扫描等实际应用的预处理流程
- [ ] 评估和优化阈值处理效果
- [ ] 绘制和分析图像直方图
- [ ] 使用形态学操作优化阈值结果

---

## 🚀 扩展挑战（可选）

完成基础任务后，可以尝试以下挑战：

### 挑战1：交互式阈值调整工具

**目标：** 实现实时调整阈值参数的可视化工具

**要求：**
- 使用 Trackbar 调整阈值、blockSize、C
- 支持切换不同阈值类型
- 实时显示处理结果
- 显示直方图和阈值位置
- 显示前景像素占比

**代码框架：**
```python
import cv2
import numpy as np

def nothing(x):
    pass

# 读取图像
img = cv2.imread('document.jpg', cv2.IMREAD_GRAYSCALE)

# 创建窗口
cv2.namedWindow('Threshold Control')

# 创建滑动条
cv2.createTrackbar('Threshold', 'Threshold Control', 127, 255, nothing)
cv2.createTrackbar('Type', 'Threshold Control', 0, 4, nothing)
cv2.createTrackbar('BlockSize', 'Threshold Control', 11, 31, nothing)
cv2.createTrackbar('C', 'Threshold Control', 2, 20, nothing)
cv2.createTrackbar('Method', 'Threshold Control', 0, 1, nothing)

while True:
    # 读取参数
    thresh_val = cv2.getTrackbarPos('Threshold', 'Threshold Control')
    type_val = cv2.getTrackbarPos('Type', 'Threshold Control')
    block_size = cv2.getTrackbarPos('BlockSize', 'Threshold Control')
    c_val = cv2.getTrackbarPos('C', 'Threshold Control')
    method_val = cv2.getTrackbarPos('Method', 'Threshold Control')

    # 确保 blockSize 为奇数
    if block_size % 2 == 0:
        block_size += 1
    if block_size < 3:
        block_size = 3

    # 阈值类型
    types = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV,
             cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV]

    # 根据方法选择处理方式
    if method_val == 0:  # 全局阈值
        ret, thresh = cv2.threshold(img, thresh_val, 255, types[type_val])
    else:  # 自适应阈值
        methods = [cv2.ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C]
        thresh = cv2.adaptiveThreshold(img, 255, methods[method_val],
                                       types[type_val], block_size, c_val)

    # 计算前景占比
    fg_ratio = (np.count_nonzero(thresh) / thresh.size) * 100

    # 显示结果和统计信息
    display = thresh.copy()
    info = f"FG: {fg_ratio:.1f}% | BS: {block_size} | C: {c_val}"
    cv2.putText(display, info, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Threshold Control', display)

    # ESC 退出
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
```

### 挑战2：多阈值分割与彩色标记

**目标：** 实现多阈值分割，用不同颜色标记不同区域

**要求：**
- 实现多阈值分割算法
- 用不同颜色标记不同灰度级区域
- 创建对比图
- 支持自定义阈值数量和位置

**代码提示：**
```python
def multi_threshold_colored(img, thresholds):
    """
    多阈值分割并彩色标记

    参数:
        img: 灰度图像
        thresholds: 阈值列表 [t1, t2, t3, ...]

    返回:
        彩色标记图像
    """
    # 定义颜色列表
    colors = [
        (0, 0, 255),      # 红色
        (0, 255, 0),      # 绿色
        (255, 0, 0),      # 蓝色
        (0, 255, 255),    # 黄色
        (255, 0, 255),    # 紫色
        (255, 255, 0),    # 青色
    ]

    result = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    # 为每个区间分配颜色
    prev_thresh = 0
    for i, thresh in enumerate(thresholds + [256]):
        mask = (img > prev_thresh) & (img <= thresh)
        result[mask] = colors[i % len(colors)]
        prev_thresh = thresh

    return result
```

### 挑战3：自动方法选择系统

**目标：** 根据图像特性自动选择最佳阈值方法

**要求：**
- 分析图像直方图特性
- 检测光照均匀程度
- 自动判断是否适合 Otsu
- 自动选择全局或自适应阈值
- 输出选择理由和参数

**代码框架：**
```python
def auto_threshold_selection(img):
    """
    自动选择最佳阈值方法

    返回:
        (方法名称, 处理结果, 选择理由)
    """
    # 1. 分析直方图
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])

    # 2. 检测光照均匀度
    std_dev = np.std(img)

    # 3. 判断是否适合 Otsu
    # (检测是否有明显的双峰)

    # 4. 根据分析结果选择方法

    # 返回结果
    return method_name, result, reason
```

### 挑战4：视频实时阈值处理

**目标：** 对视频进行实时阈值处理

**要求：**
- 从摄像头或视频文件读取
- 实时应用阈值处理
- 支持切换不同方法
- 显示处理帧率
- 保存处理结果

**代码提示：**
```python
import cv2
import time

# 打开摄像头
cap = cv2.VideoCapture(0)  # 或 'video.mp4'

prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 转灰度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 应用阈值（选择一种方法）
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # 计算帧率
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # 显示 FPS
    cv2.putText(thresh, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Threshold', thresh)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

### 挑战5：文档扫描完整应用

**目标：** 实现完整的文档扫描应用

**要求：**
- 自动检测文档边缘
- 透视变换矫正文档
- 自适应阈值二值化
- 形态学去噪
- 输出高质量扫描结果

**参考流程：**
```python
def scan_document(image_path):
    """
    完整的文档扫描流程
    """
    # 1. 读取图像
    img = cv2.imread(image_path)

    # 2. 预处理（灰度 + 滤波 + 边缘检测）

    # 3. 查找文档轮廓

    # 4. 透视变换矫正

    # 5. 自适应阈值

    # 6. 形态学去噪

    # 7. 保存结果
    return result
```

---

**祝你好运！佛祖保佑，永无BUG！🙏**
