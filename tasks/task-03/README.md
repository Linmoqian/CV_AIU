# Task 3: 图像滤波与去噪

## 📚 学习目标

通过完成本任务,你将掌握：
- ✅ 理解图像噪声的类型（高斯噪声、椒盐噪声）
- ✅ 掌握常用的线性滤波方法（均值滤波、高斯滤波）
- ✅ 掌握非线性滤波方法（中值滤波、双边滤波）
- ✅ 理解卷积核的概念和作用
- ✅ 掌握自定义卷积核实现图像锐化
- ✅ 掌握边缘检测算法（Sobel、Canny）
- ✅ 理解不同滤波方法的适用场景
- ✅ 学会评估滤波效果（PSNR、SSIM等指标）

## 🎯 任务概述

本任务要求你使用多种滤波方法对含噪图像进行去噪处理，并对比分析各种方法的效果。图像滤波是计算机视觉中的基础操作，广泛应用于图像去噪、边缘检测、特征提取等场景。你将实现线性滤波、非线性滤波、自定义锐化核以及边缘检测算法，并分析它们的优缺点。

**预计时间：** 60-90 分钟
**难度：** ⭐⭐⭐☆☆

## 📋 前置知识

在开始之前，确保你已经：
- [ ] 完成了 [Task 1: 图像基本操作](../task-01/README.md)
- [ ] 完成了 [Task 2: 色彩空间转换](../task-02/README.md)
- [ ] 阅读 [04-图像滤波与去噪](../../docs/04-图像滤波与去噪.md)
- [ ] 理解卷积运算的基本概念
- [ ] 理解图像噪声的类型和特点

## 🔧 开发环境

```bash
# 确保已安装必要的库
pip install opencv-python numpy matplotlib

# 测试图片位置
../../assets/sample-images/noisy/
```

**推荐测试图像：**
- `noisy-gaussian.jpg` - 包含高斯噪声的图像
- `noisy-salt-pepper.jpg` - 包含椒盐噪声的图像
- 或自行对清晰图像添加噪声进行测试

## 📝 任务要求

### 1. 线性滤波：均值滤波与高斯滤波（25分）

**目标：** 掌握线性滤波方法，理解其原理和效果差异

**要求：**
1. **均值滤波（Mean Filter）**
   - 使用 `cv2.blur()` 实现
   - 尝试不同的核大小（3x3, 5x5, 7x7）
   - 保存结果为 `filtering_mean_5x5.jpg`
   - 分析核大小对滤波效果的影响

2. **高斯滤波（Gaussian Filter）**
   - 使用 `cv2.GaussianBlur()` 实现
   - 理解 sigmaX 和 sigmaY 参数的作用
   - 保存结果为 `filtering_gaussian_5x5.jpg`
   - 对比均值滤波和高斯滤波的差异

**核心代码：**
```python
import cv2
import numpy as np

# 读取含噪图像
img = cv2.imread('noisy-gaussian.jpg')

# 1. 均值滤波
# 核大小必须为正奇数
mean_3x3 = cv2.blur(img, (3, 3))
mean_5x5 = cv2.blur(img, (5, 5))
mean_7x7 = cv2.blur(img, (7, 7))

cv2.imwrite('filtering_mean_3x3.jpg', mean_3x3)
cv2.imwrite('filtering_mean_5x5.jpg', mean_5x5)
cv2.imwrite('filtering_mean_7x7.jpg', mean_7x7)

# 2. 高斯滤波
# sigmaX=0 表示根据核大小自动计算
gaussian_3x3 = cv2.GaussianBlur(img, (3, 3), 0)
gaussian_5x5 = cv2.GaussianBlur(img, (5, 5), 0)
gaussian_7x7 = cv2.GaussianBlur(img, (7, 7), 0)

# 也可以指定 sigma 值
gaussian_custom = cv2.GaussianBlur(img, (5, 5), sigmaX=1.5)

cv2.imwrite('filtering_gaussian_5x5.jpg', gaussian_5x5)
cv2.imwrite('filtering_gaussian_7x7.jpg', gaussian_7x7)

print(f"均值滤波 3x3: {mean_3x3.shape}")
print(f"高斯滤波 5x5: {gaussian_5x5.shape}")
```

**原理解析：**

**均值滤波：**
- 使用均匀权重的卷积核
- 核内所有像素权重相同
- 优点：计算简单快速
- 缺点：会模糊边缘，对椒盐噪声效果差

**高斯滤波：**
- 使用高斯分布的权重
- 中心像素权重最大，向外递减
- 优点：保留边缘较好，平滑效果自然
- 缺点：计算量稍大

**提示：**
- 核越大，滤波效果越明显，但图像也越模糊
- 高斯滤波的 sigma 参数控制平滑程度
- 两种滤波都对高斯噪声有效，对椒盐噪声效果差

---

### 2. 非线性滤波：中值滤波与双边滤波（30分）

**目标：** 掌握非线性滤波方法，理解其优势

**要求：**
1. **中值滤波（Median Filter）**
   - 使用 `cv2.medianBlur()` 实现
   - 对椒盐噪声图像进行处理
   - 保存结果为 `filtering_median_5x5.jpg`
   - 对比其在线性和非线性滤波中的表现

2. **双边滤波（Bilateral Filter）**
   - 使用 `cv2.bilateralFilter()` 实现
   - 理解 d、sigmaColor、sigmaSpace 三个参数
   - 保存结果为 `filtering_bilateral.jpg`
   - 观察其边缘保留能力

**核心代码：**
```python
# 读取椒盐噪声图像
img_sp = cv2.imread('noisy-salt-pepper.jpg')

# 1. 中值滤波
# 核大小必须为正奇数（1, 3, 5, 7...）
median_3x3 = cv2.medianBlur(img_sp, 3)
median_5x5 = cv2.medianBlur(img_sp, 5)
median_7x7 = cv2.medianBlur(img_sp, 7)

cv2.imwrite('filtering_median_3x3.jpg', median_3x3)
cv2.imwrite('filtering_median_5x5.jpg', median_5x5)
cv2.imwrite('filtering_median_7x7.jpg', median_7x7)

# 2. 双边滤波
# d: 滤波过程中每个像素邻域的直径
# sigmaColor: 颜色空间的标准差，越大表示颜色差异大的像素也会互相影响
# sigmaSpace: 坐标空间的标准差，越大表示距离远的像素也会互相影响

# 参数1: 保守设置，边缘保留好，去噪弱
bilateral_1 = cv2.bilateralFilter(img, 9, 75, 75)

# 参数2: 中等设置
bilateral_2 = cv2.bilateralFilter(img, 15, 80, 80)

# 参数3: 激进设置，去噪强，但可能过度平滑
bilateral_3 = cv2.bilateralFilter(img, 25, 100, 100)

cv2.imwrite('filtering_bilateral_1.jpg', bilateral_1)
cv2.imwrite('filtering_bilateral_2.jpg', bilateral_2)
cv2.imwrite('filtering_bilateral_3.jpg', bilateral_3)
```

**原理解析：**

**中值滤波：**
- 取邻域内像素的中值
- 对极值（黑白噪点）不敏感
- 优点：对椒盐噪声效果最好，保留边缘
- 缺点：计算量大（需要排序），对高斯噪声效果一般

**双边滤波：**
- 同时考虑空间距离和颜色差异
- 只有空间接近且颜色相似的像素才互相影响
- 优点：保留边缘的同时去噪（美颜效果）
- 缺点：计算量大，速度慢

**参数调优指南：**

| 参数 | 推荐值 | 效果 |
|------|--------|------|
| d | 5-15 | 值越大去噪越强，但速度越慢 |
| sigmaColor | 50-150 | 值越大，颜色差异大的像素也会混合 |
| sigmaSpace | 50-150 | 值越大，距离远的像素也会影响 |

**提示：**
- 中值滤波是处理椒盐噪声的首选
- 双边滤波适合需要保留边缘的场景（如人像磨皮）
- 双边滤波参数需要根据图像内容调整

---

### 3. 效果对比与分析（25分）

**目标：** 全面对比各种滤波方法的效果，分析适用场景

**要求：**
1. **创建对比图像**
   - 将所有滤波结果并排显示
   - 使用 `np.hstack()` 和 `np.vstack()` 组合
   - 保存为 `filtering_comparison.jpg`

2. **定量分析**
   - 计算滤波前后的 PSNR（峰值信噪比）
   - 统计计算时间
   - 记录各参数设置

3. **定性分析**
   - 观察各种滤波方法的视觉效果
   - 分析边缘保留情况
   - 评估去噪程度

**完整代码框架：**
```python
import cv2
import numpy as np
import time

def calculate_psnr(img1, img2):
    """
    计算两幅图像的PSNR（峰值信噪比）
    值越大表示图像质量越好
    """
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    if mse == 0:
        return float('inf')
    pixel_max = 255.0
    psnr = 20 * np.log10(pixel_max / np.sqrt(mse))
    return psnr

# 读取原图和含噪图像
original = cv2.imread('original.jpg')
noisy = cv2.imread('noisy-gaussian.jpg')

# 存储结果和计时
results = []
times = {}
psnrs = {}

# 1. 均值滤波
start = time.time()
mean_filtered = cv2.blur(noisy, (5, 5))
times['mean'] = time.time() - start
psnrs['mean'] = calculate_psnr(original, mean_filtered)
results.append(mean_filtered)

# 2. 高斯滤波
start = time.time()
gaussian_filtered = cv2.GaussianBlur(noisy, (5, 5), 0)
times['gaussian'] = time.time() - start
psnrs['gaussian'] = calculate_psnr(original, gaussian_filtered)
results.append(gaussian_filtered)

# 3. 中值滤波
start = time.time()
median_filtered = cv2.medianBlur(noisy, 5)
times['median'] = time.time() - start
psnrs['median'] = calculate_psnr(original, median_filtered)
results.append(median_filtered)

# 4. 双边滤波
start = time.time()
bilateral_filtered = cv2.bilateralFilter(noisy, 9, 75, 75)
times['bilateral'] = time.time() - start
psnrs['bilateral'] = calculate_psnr(original, bilateral_filtered)
results.append(bilateral_filtered)

# 创建对比图（2行3列）
# 第一行：原图、含噪图、均值滤波
# 第二行：高斯、中值、双边
row1 = np.hstack([original, noisy, mean_filtered])
row2 = np.hstack([gaussian_filtered, median_filtered, bilateral_filtered])
comparison = np.vstack([row1, row2])

# 缩放到合适大小显示
comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
cv2.imwrite('filtering_comparison.jpg', comparison)

# 打印统计信息
print("=" * 60)
print("滤波效果对比分析")
print("=" * 60)
print(f"{'方法':<15} {'时间(ms)':<12} {'PSNR(dB)':<12}")
print("-" * 60)
for method in ['mean', 'gaussian', 'median', 'bilateral']:
    print(f"{method:<15} {times[method]*1000:<12.2f} {psnrs[method]:<12.2f}")
print("=" * 60)
```

**分析报告模板：**
```python
analysis_report = """
# 图像滤波效果分析报告

## 1. 均值滤波 (Mean Filter)
- **原理**: 使用均匀权重卷积核
- **优点**: 计算快速，实现简单
- **缺点**: 模糊边缘严重，对椒盐噪声效果差
- **适用场景**: 轻微高斯噪声，对实时性要求高的场景
- **PSNR**: {:.2f} dB
- **处理时间**: {:.2f} ms

## 2. 高斯滤波 (Gaussian Filter)
- **原理**: 使用高斯分布权重
- **优点**: 保留边缘较好，平滑自然
- **缺点**: 对椒盐噪声效果差
- **适用场景**: 高斯噪声，预处理的平滑操作
- **PSNR**: {:.2f} dB
- **处理时间**: {:.2f} ms

## 3. 中值滤波 (Median Filter)
- **原理**: 取邻域中值
- **优点**: 对椒盐噪声效果最好，保留边缘
- **缺点**: 计算量大（需要排序）
- **适用场景**: 椒盐噪声，脉冲噪声
- **PSNR**: {:.2f} dB
- **处理时间**: {:.2f} ms

## 4. 双边滤波 (Bilateral Filter)
- **原理**: 同时考虑空间距离和颜色差异
- **优点**: 保留边缘的同时去噪
- **缺点**: 计算量很大，速度慢
- **适用场景**: 需要保留边缘的去噪（美颜、磨皮）
- **PSNR**: {:.2f} dB
- **处理时间**: {:.2f} ms

## 总结
根据PSNR和处理时间综合评估，
{}滤波效果最好，但速度{}。
"""

print(analysis_report.format(
    psnrs['mean'], times['mean']*1000,
    psnrs['gaussian'], times['gaussian']*1000,
    psnrs['median'], times['median']*1000,
    psnrs['bilateral'], times['bilateral']*1000,
    best_method,
    "较慢" if best_method in ['bilateral', 'median'] else "较快"
))

# 保存报告到文件
with open('filtering_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write(analysis_report.format(
        psnrs['mean'], times['mean']*1000,
        psnrs['gaussian'], times['gaussian']*1000,
        psnrs['median'], times['median']*1000,
        psnrs['bilateral'], times['bilateral']*1000,
        best_method,
        "较慢" if best_method in ['bilateral', 'median'] else "较快"
    ))
```

---

### 4. 自定义锐化卷积核（20分）

**目标：** 理解卷积核的工作原理，实现图像锐化

**要求：**
1. **设计锐化核**
   - 创建 3x3 锐化卷积核
   - 中心值为正，周围为负
   - 所有元素之和为 1（保持亮度）

2. **应用锐化核**
   - 使用 `cv2.filter2D()` 应用自定义核
   - 对模糊图像进行锐化
   - 保存结果为 `sharpened_custom.jpg`

3. **对比效果**
   - 对比锐化前后的差异
   - 调整核的强度参数

**核心代码：**
```python
# 读取模糊图像或使用之前滤波后的图像
blur_img = cv2.imread('blur_image.jpg')
# 或者对清晰图像先模糊再锐化
blur_img = cv2.GaussianBlur(original, (7, 7), 0)

# 方法1: 基础锐化核
# 锐化原理: 增强中心像素与周围像素的对比
kernel_sharpen_1 = np.array([
    [-1, -1, -1],
    [-1,  9, -1],
    [-1, -1, -1]
])

# 方法2: 拉普拉斯锐化核
kernel_sharpen_2 = np.array([
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0]
])

# 方法3: 可调强度的锐化核
def create_sharpen_kernel(strength=1.0):
    """
    创建可调强度的锐化核

    参数:
        strength: 锐化强度，0.1-3.0
                 值越大锐化越强
    """
    base = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    # 调整中心值
    base[1, 1] = 4 * strength + 1
    return base

# 应用锐化核
sharpened_1 = cv2.filter2D(blur_img, -1, kernel_sharpen_1)
sharpened_2 = cv2.filter2D(blur_img, -1, kernel_sharpen_2)

# 使用不同强度的锐化
for strength in [0.5, 1.0, 1.5, 2.0]:
    kernel = create_sharpen_kernel(strength)
    sharpened = cv2.filter2D(blur_img, -1, kernel)
    cv2.imwrite(f'sharpened_strength_{strength}.jpg', sharpened)

# 保存结果
cv2.imwrite('sharpened_custom.jpg', sharpened_1)

# 创建对比图
comparison = np.hstack([
    original,
    blur_img,
    sharpened_1
])
# 调整大小并保存
comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
cv2.imwrite('sharpen_comparison.jpg', comparison)

print("锐化核 1:")
print(kernel_sharpen_1)
print("\n锐化核 2:")
print(kernel_sharpen_2)
print(f"核1元素和: {kernel_sharpen_1.sum()}")
print(f"核2元素和: {kernel_sharpen_2.sum()}")
```

**锐化原理：**

锐化的本质是增强边缘，即增强像素之间的差异。常见的锐化核包括：

1. **高强度锐化核：**
   ```
   [-1, -1, -1]
   [-1,  9, -1]
   [-1, -1, -1]
   ```
   - 效果强烈，可能引入噪声
   - 适合严重模糊的图像

2. **拉普拉斯锐化核：**
   ```
   [ 0, -1,  0]
   [-1,  5, -1]
   [ 0, -1,  0]
   ```
   - 效果适中，较为常用
   - 考虑了上下左右4个方向

3. **对角线锐化核：**
   ```
   [-1, -1, -1]
   [-1,  8, -1]
   [-1, -1, -1]
   ```
   - 考虑了所有8个方向
   - 元素和为0，提取的是边缘信息

**提示：**
- 锐化核所有元素之和应为1，以保持图像整体亮度
- 锐化强度过大可能引入噪声或产生过度锐化的伪影
- 可以先锐化再与原图按比例混合，获得更自然的效果

```python
# 混合锐化效果
alpha = 0.7  # 原图权重
beta = 0.3   # 锐化图权重
sharpened_blended = cv2.addWeighted(original, alpha, sharpened_1, beta, 0)
cv2.imwrite('sharpened_blended.jpg', sharpened_blended)
```

---

### 5. 边缘检测：Sobel 与 Canny（30分）

**目标：** 掌握常用的边缘检测算法，理解其原理和差异

**要求：**
1. **Sobel 边缘检测**
   - 使用 `cv2.Sobel()` 计算梯度
   - 分别计算 x 方向和 y 方向的梯度
   - 合并为梯度幅值
   - 保存结果为 `edges_sobel.jpg`

2. **Canny 边缘检测**
   - 使用 `cv2.Canny()` 实现边缘检测
   - 理解双阈值的作用
   - 调整阈值参数优化效果
   - 保存结果为 `edges_canny.jpg`

3. **对比分析**
   - 对比两种方法的检测结果
   - 分析各自的特点
   - 说明适用场景

**完整代码框架：**
```python
import cv2
import numpy as np

# 读取图像并转换为灰度图
img = cv2.imread('original.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ==================== Sobel 边缘检测 ====================
print("Sobel 边缘检测...")

# 计算x方向梯度
# cv2.CV_64F: 使用64位浮点数，可以存储负值
# 1, 0: 表示x方向求导
# ksize=3: Sobel核大小，必须是1, 3, 5或7
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)

# 计算y方向梯度
# 0, 1: 表示y方向求导
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

# 转换为绝对值并转为uint8
sobelx = np.uint8(np.absolute(sobelx))
sobely = np.uint8(np.absolute(sobely))

# 合并x和y方向的梯度
# 方法1: 直接相加
sobelxy1 = cv2.add(sobelx, sobely)

# 方法2: 计算梯度幅值（更准确）
sobelxy2 = np.sqrt(sobelx.astype(float)**2 + sobely.astype(float)**2)
sobelxy2 = np.uint8(sobelxy2 / sobelxy2.max() * 255)

cv2.imwrite('edges_sobel_x.jpg', sobelx)
cv2.imwrite('edges_sobel_y.jpg', sobely)
cv2.imwrite('edges_sobel_xy.jpg', sobelxy2)

print(f"  [OK] Sobel X方向: {sobelx.shape}")
print(f"  [OK] Sobel Y方向: {sobely.shape}")
print(f"  [OK] Sobel合并: {sobelxy2.shape}")

# ==================== Canny 边缘检测 ====================
print("\nCanny 边缘检测...")

# Canny边缘检测的三个步骤:
# 1. 高斯滤波降噪
# 2. 计算梯度幅值和方向
# 3. 双阈值检测和边缘连接

# 参数说明:
# threshold1: 低阈值，用于检测弱边缘
# threshold2: 高阈值，用于检测强边缘
# 推荐比例: 高阈值 = 低阈值 * 2-3

# 不同阈值设置
canny_1 = cv2.Canny(gray, 50, 150)    # 低阈值
canny_2 = cv2.Canny(gray, 100, 200)   # 中阈值
canny_3 = cv2.Canny(gray, 150, 300)   # 高阈值

# 更精细的阈值（适合细节多的图像）
canny_fine = cv2.Canny(gray, 30, 100)

cv2.imwrite('edges_canny_50_150.jpg', canny_1)
cv2.imwrite('edges_canny_100_200.jpg', canny_2)
cv2.imwrite('edges_canny_150_300.jpg', canny_3)
cv2.imwrite('edges_canny_fine.jpg', canny_fine)

print(f"  [OK] Canny 50-150: {canny_1.shape}")
print(f"  [OK] Canny 100-200: {canny_2.shape}")
print(f"  [OK] Canny 150-300: {canny_3.shape}")

# ==================== 对比显示 ====================
print("\n创建对比图...")

# 创建Sobel对比图
sobel_comparison = np.hstack([
    cv2.cvtColor(sobelx, cv2.COLOR_GRAY2BGR),
    cv2.cvtColor(sobely, cv2.COLOR_GRAY2BGR),
    cv2.cvtColor(sobelxy2, cv2.COLOR_GRAY2BGR)
])

# 创建Canny对比图
canny_comparison = np.hstack([
    cv2.cvtColor(canny_1, cv2.COLOR_GRAY2BGR),
    cv2.cvtColor(canny_2, cv2.COLOR_GRAY2BGR),
    cv2.cvtColor(canny_3, cv2.COLOR_GRAY2BGR)
])

# 合并所有对比图
all_edges = np.vstack([sobel_comparison, canny_comparison])
all_edges = cv2.resize(all_edges, None, fx=0.5, fy=0.5)
cv2.imwrite('edges_comparison.jpg', all_edges)

# ==================== 统计边缘像素 ====================
def count_edge_pixels(edge_img):
    """统计边缘像素数量"""
    return np.count_nonzero(edge_img)

print("\n边缘像素统计:")
print(f"  - Sobel X: {count_edge_pixels(sobelx)} 个像素")
print(f"  - Sobel Y: {count_edge_pixels(sobely)} 个像素")
print(f"  - Sobel XY: {count_edge_pixels(sobelxy2)} 个像素")
print(f"  - Canny (50-150): {count_edge_pixels(canny_1)} 个像素")
print(f"  - Canny (100-200): {count_edge_pixels(canny_2)} 个像素")
print(f"  - Canny (150-300): {count_edge_pixels(canny_3)} 个像素")

print("\n所有边缘检测完成！")
```

**Sobel vs Canny 对比：**

| 特性 | Sobel | Canny |
|------|-------|-------|
| **原理** | 一阶微分算子 | 多阶段算法（降噪-梯度-非极大值抑制-双阈值） |
| **输出** | 灰度图（梯度强度） | 二值图（边缘/非边缘） |
| **边缘宽度** | 较宽 | 单像素宽 |
| **噪声敏感度** | 较高 | 较低（先高斯滤波） |
| **参数调节** | 较少（ksize） | 需要调整双阈值 |
| **计算速度** | 快 | 较慢 |
| **适用场景** | 简单边缘检测，梯度计算 | 精确边缘检测，需要细化边缘 |

**阈值选择指南：**

```python
# 自适应阈值选择（基于图像统计）
def auto_canny_threshold(image, sigma=0.33):
    """
    自动计算Canny阈值

    参数:
        image: 输入灰度图像
        sigma: 用于计算阈值的参数（0.1-0.5）

    返回:
        (低阈值, 高阈值)
    """
    # 计算图像中值
    v = np.median(image)

    # 计算阈值
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    return lower, upper

# 使用自动阈值
lower, upper = auto_canny_threshold(gray)
canny_auto = cv2.Canny(gray, lower, upper)
cv2.imwrite('edges_canny_auto.jpg', canny_auto)
print(f"自动阈值: {lower}, {upper}")
```

**提示：**
- Sobel 适合梯度分析和方向性边缘检测
- Canny 适合需要精确边缘的场景
- 低阈值控制边缘检测的敏感度
- 高阈值控制强边缘的选择
- 阈值需要根据图像内容调整

---

## 📦 提交要求

### 必交内容

1. **代码文件**：`task3_solution.py`
   - 包含所有四个任务的实现
   - 代码注释清晰，符合 PEP 8 规范
   - 包含滤波效果分析函数

2. **保存的图像**（按任务要求命名）：
   ```
   filtering_mean_5x5.jpg          # 均值滤波
   filtering_gaussian_5x5.jpg      # 高斯滤波
   filtering_median_5x5.jpg        # 中值滤波
   filtering_bilateral.jpg         # 双边滤波
   filtering_comparison.jpg        # 滤波效果对比图
   sharpened_custom.jpg            # 自定义锐化结果
   edges_sobel.jpg                 # Sobel边缘检测
   edges_canny.jpg                 # Canny边缘检测
   edges_comparison.jpg            # 边缘检测对比图
   ```

3. **分析报告**：`filtering_analysis_report.txt` 或 `report.md`
   - 包含各种滤波方法的原理说明
   - PSNR 和处理时间对比
   - 适用场景分析
   - 至少 300 字

4. **运行结果截图**：`result_screenshot.png`
   - 显示程序运行的控制台输出
   - 包含 PSNR 和时间统计信息

### 提交格式

```
task-03-submission/
├── task3_solution.py              # 你的代码
├── result_screenshot.png          # 运行结果截图
├── filtering_analysis_report.txt  # 分析报告
├── output_images/                 # 输出图像文件夹
│   ├── filtering_mean_5x5.jpg
│   ├── filtering_gaussian_5x5.jpg
│   ├── filtering_median_5x5.jpg
│   ├── filtering_bilateral.jpg
│   ├── filtering_comparison.jpg
│   ├── sharpened_custom.jpg
│   ├── edges_sobel.jpg
│   ├── edges_canny.jpg
│   └── edges_comparison.jpg
└── report.md                       # 实验报告（可选）
```

---

## 📊 评分标准

| 任务项 | 分值 | 评分标准 |
|--------|------|----------|
| **1. 线性滤波** | 25分 | |
| - 均值滤波实现 | 10分 | 正确使用 cv2.blur，尝试不同核大小 |
| - 高斯滤波实现 | 10分 | 正确使用 GaussianBlur，理解sigma参数 |
| - 原理说明 | 5分 | 清晰说明两种滤波的差异 |
| **2. 非线性滤波** | 30分 | |
| - 中值滤波实现 | 12分 | 正确使用 medianBlur，效果良好 |
| - 双边滤波实现 | 12分 | 正确使用 bilateralFilter，参数合理 |
| - 参数调优 | 6分 | 尝试不同参数组合并分析效果 |
| **3. 效果对比分析** | 25分 | |
| - 对比图制作 | 8分 | 创建清晰的对比图，布局合理 |
| - PSNR计算 | 8分 | 正确计算并解释PSNR含义 |
| - 分析报告 | 9分 | 报告完整，分析深入，至少300字 |
| **4. 自定义锐化核** | 20分 | |
| - 锐化核设计 | 8分 | 核设计正确，元素和为1 |
| - 滤波效果 | 7分 | 锐化效果明显，不过度 |
| - 可调强度 | 5分 | 实现可调强度的锐化函数 |
| **5. 边缘检测** | 30分 | |
| - Sobel实现 | 12分 | 正确计算x/y方向梯度并合并 |
| - Canny实现 | 12分 | 正确使用双阈值，效果良好 |
| - 对比分析 | 6分 | 清晰对比两种方法的差异 |
| **代码质量** | +10分 | |
| - 注释清晰 | +4分 | 代码有详细的中文注释 |
| - 代码规范 | +3分 | 符合 PEP 8 规范 |
| - 错误处理 | +3分 | 有完善的异常处理机制 |
| **额外加分项** | +20分 | |
| - 自动阈值选择 | +5分 | 实现自适应Canny阈值 |
| - 可视化增强 | +5分 | 使用matplotlib绘制效果曲线 |
| - 交互式调参 | +5分 | 使用Trackbar实时调整参数 |
| - 多种噪声测试 | +5分 | 测试不同噪声类型的效果 |

**总分：130分 + 10分（代码质量）+ 20分（额外加分）= 160分**

---

## 💡 完整代码框架

```python
"""
Task 3: 图像滤波与去噪
姓名：[你的名字]
学号：[你的学号]
日期：[提交日期]
"""

import cv2
import numpy as np
import time
import sys
import os

# ==================== 配置区 ====================
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

# 图片路径
ORIGINAL_PATH = 'sample-images/basic/landscape.jpg'
NOISY_GAUSSIAN_PATH = 'sample-images/noisy/noisy-gaussian.jpg'
NOISY_SALT_PEPPER_PATH = 'sample-images/noisy/noisy-salt-pepper.jpg'
OUTPUT_DIR = 'output_images'

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 工具函数 ====================
def calculate_psnr(img1, img2):
    """计算两幅图像的PSNR（峰值信噪比）"""
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    if mse == 0:
        return float('inf')
    pixel_max = 255.0
    psnr = 20 * np.log10(pixel_max / np.sqrt(mse))
    return psnr

def auto_canny_threshold(image, sigma=0.33):
    """自动计算Canny阈值"""
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    return lower, upper

def create_sharpen_kernel(strength=1.0):
    """创建可调强度的锐化核"""
    base = np.array([
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ])
    base[1, 1] = 4 * strength + 1
    return base

# ==================== 主程序 ====================
print("=" * 70)
print("Task 3: 图像滤波与去噪")
print("=" * 70)

# 1. 读取图像
print("\n[1] 读取图像...")
original = imread_chinese(get_image_path(ORIGINAL_PATH))
noisy_gaussian = imread_chinese(get_image_path(NOISY_GAUSSIAN_PATH))
noisy_sp = imread_chinese(get_image_path(NOISY_SALT_PEPPER_PATH))

if original is None or noisy_gaussian is None or noisy_sp is None:
    print("  [ERROR] 图片读取失败！")
    sys.exit(1)

print(f"  [OK] 原图: {original.shape}")
print(f"  [OK] 高斯噪声图: {noisy_gaussian.shape}")
print(f"  [OK] 椒盐噪声图: {noisy_sp.shape}")

# 2. 线性滤波
print("\n[2] 线性滤波...")

# 均值滤波
start = time.time()
mean_5x5 = cv2.blur(noisy_gaussian, (5, 5))
mean_time = time.time() - start
mean_psnr = calculate_psnr(original, mean_5x5)
cv2.imwrite(f'{OUTPUT_DIR}/filtering_mean_5x5.jpg', mean_5x5)
print(f"  [OK] 均值滤波 5x5: PSNR={mean_psnr:.2f}dB, 时间={mean_time*1000:.2f}ms")

# 高斯滤波
start = time.time()
gaussian_5x5 = cv2.GaussianBlur(noisy_gaussian, (5, 5), 0)
gaussian_time = time.time() - start
gaussian_psnr = calculate_psnr(original, gaussian_5x5)
cv2.imwrite(f'{OUTPUT_DIR}/filtering_gaussian_5x5.jpg', gaussian_5x5)
print(f"  [OK] 高斯滤波 5x5: PSNR={gaussian_psnr:.2f}dB, 时间={gaussian_time*1000:.2f}ms")

# 3. 非线性滤波
print("\n[3] 非线性滤波...")

# 中值滤波
start = time.time()
median_5x5 = cv2.medianBlur(noisy_sp, 5)
median_time = time.time() - start
median_psnr = calculate_psnr(original, median_5x5)
cv2.imwrite(f'{OUTPUT_DIR}/filtering_median_5x5.jpg', median_5x5)
print(f"  [OK] 中值滤波 5x5: PSNR={median_psnr:.2f}dB, 时间={median_time*1000:.2f}ms")

# 双边滤波
start = time.time()
bilateral = cv2.bilateralFilter(noisy_gaussian, 9, 75, 75)
bilateral_time = time.time() - start
bilateral_psnr = calculate_psnr(original, bilateral)
cv2.imwrite(f'{OUTPUT_DIR}/filtering_bilateral.jpg', bilateral)
print(f"  [OK] 双边滤波: PSNR={bilateral_psnr:.2f}dB, 时间={bilateral_time*1000:.2f}ms")

# 4. 创建滤波对比图
print("\n[4] 创建滤波对比图...")
row1 = np.hstack([original, noisy_gaussian, mean_5x5])
row2 = np.hstack([gaussian_5x5, median_5x5, bilateral])
comparison = np.vstack([row1, row2])
comparison = cv2.resize(comparison, None, fx=0.5, fy=0.5)
cv2.imwrite(f'{OUTPUT_DIR}/filtering_comparison.jpg', comparison)
print(f"  [OK] 对比图已保存")

# 5. 自定义锐化
print("\n[5] 自定义锐化核...")
blur_img = cv2.GaussianBlur(original, (7, 7), 0)
kernel_sharpen = create_sharpen_kernel(strength=1.0)
sharpened = cv2.filter2D(blur_img, -1, kernel_sharpen)
cv2.imwrite(f'{OUTPUT_DIR}/sharpened_custom.jpg', sharpened)
print(f"  [OK] 锐化核:\n{kernel_sharpen}")

# 6. 边缘检测
print("\n[6] 边缘检测...")
gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

# Sobel
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobelx = np.uint8(np.absolute(sobelx))
sobely = np.uint8(np.absolute(sobely))
sobelxy = np.uint8(np.sqrt(sobelx.astype(float)**2 + sobely.astype(float)**2))
sobelxy = np.uint8(sobelxy / sobelxy.max() * 255)
cv2.imwrite(f'{OUTPUT_DIR}/edges_sobel.jpg', sobelxy)
print(f"  [OK] Sobel边缘检测完成")

# Canny
lower, upper = auto_canny_threshold(gray)
canny = cv2.Canny(gray, lower, upper)
cv2.imwrite(f'{OUTPUT_DIR}/edges_canny.jpg', canny)
print(f"  [OK] Canny边缘检测完成 (阈值: {lower}-{upper})")

# 7. 生成分析报告
print("\n[7] 生成分析报告...")
report = f"""
# 图像滤波效果分析报告

## 测试图像
- 原图尺寸: {original.shape}
- 高斯噪声图: {noisy_gaussian.shape}
- 椒盐噪声图: {noisy_sp.shape}

## 线性滤波结果

### 1. 均值滤波 (Mean Filter)
- **原理**: 使用均匀权重卷积核，计算邻域平均值
- **PSNR**: {mean_psnr:.2f} dB
- **处理时间**: {mean_time*1000:.2f} ms
- **优点**: 计算简单快速
- **缺点**: 模糊边缘严重，对椒盐噪声效果差
- **适用场景**: 轻微高斯噪声，实时性要求高的场景

### 2. 高斯滤波 (Gaussian Filter)
- **原理**: 使用高斯分布权重，中心权重最大
- **PSNR**: {gaussian_psnr:.2f} dB
- **处理时间**: {gaussian_time*1000:.2f} ms
- **优点**: 保留边缘较好，平滑效果自然
- **缺点**: 对椒盐噪声效果差
- **适用场景**: 高斯噪声，图像预处理

## 非线性滤波结果

### 3. 中值滤波 (Median Filter)
- **原理**: 取邻域像素的中值
- **PSNR**: {median_psnr:.2f} dB
- **处理时间**: {median_time*1000:.2f} ms
- **优点**: 对椒盐噪声效果最好，保留边缘
- **缺点**: 计算量大（需要排序）
- **适用场景**: 椒盐噪声，脉冲噪声

### 4. 双边滤波 (Bilateral Filter)
- **原理**: 同时考虑空间距离和颜色差异
- **PSNR**: {bilateral_psnr:.2f} dB
- **处理时间**: {bilateral_time*1000:.2f} ms
- **优点**: 保留边缘的同时去噪（美颜效果）
- **缺点**: 计算量很大，速度慢
- **适用场景**: 需要保留边缘的去噪（美颜、磨皮）

## 边缘检测结果

### 5. Sobel边缘检测
- **原理**: 一阶微分算子，计算图像梯度
- **输出**: 灰度图（梯度强度）
- **特点**: 计算快速，可检测方向性边缘
- **适用场景**: 简单边缘检测，梯度分析

### 6. Canny边缘检测
- **原理**: 多阶段算法（降噪-梯度-非极大值抑制-双阈值）
- **阈值范围**: {lower}-{upper}
- **输出**: 二值图（边缘/非边缘）
- **特点**: 边缘细化，抗噪能力强
- **适用场景**: 精确边缘检测，需要单像素宽边缘

## 总结

1. **去噪效果排序**:
   - 高斯噪声: {'高斯滤波' if gaussian_psnr > mean_psnr else '均值滤波'} > {'均值滤波' if gaussian_psnr > mean_psnr else '高斯滤波'}
   - 椒盐噪声: 中值滤波效果最好

2. **速度排序**: 均值 > 高斯 > 中值 > 双边

3. **边缘保留**: 双边 > 高斯 > 均值

4. **推荐使用场景**:
   - 实时去噪: 均值或高斯滤波
   - 椒盐噪声: 中值滤波
   - 美颜磨皮: 双边滤波
   - 边缘检测: Canny算法
"""

with open(f'{OUTPUT_DIR}/filtering_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)
print(f"  [OK] 分析报告已保存")

# 打印统计表格
print("\n" + "=" * 70)
print("滤波方法综合对比")
print("=" * 70)
print(f"{'方法':<15} {'PSNR(dB)':<12} {'时间(ms)':<12} {'适用场景':<20}")
print("-" * 70)
print(f"{'均值滤波':<15} {mean_psnr:<12.2f} {mean_time*1000:<12.2f} {'高斯噪声':<20}")
print(f"{'高斯滤波':<15} {gaussian_psnr:<12.2f} {gaussian_time*1000:<12.2f} {'高斯噪声':<20}")
print(f"{'中值滤波':<15} {median_psnr:<12.2f} {median_time*1000:<12.2f} {'椒盐噪声':<20}")
print(f"{'双边滤波':<15} {bilateral_psnr:<12.2f} {bilateral_time*1000:<12.2f} {'保留边缘':<20}")
print("=" * 70)

# ==================== 完成 ====================
print("\n所有操作完成！")
print(f"输出目录: {OUTPUT_DIR}/")
print("=" * 70)
```

---

## 🐛 调试技巧

### 常见错误及解决方法

#### 1. 滤波效果不理想
```python
# ❌ 错误做法：核大小固定
blur = cv2.blur(img, (5, 5))

# ✅ 正确做法：根据噪声程度调整核大小
if noise_level == 'low':
    blur = cv2.blur(img, (3, 3))
elif noise_level == 'medium':
    blur = cv2.blur(img, (5, 5))
else:
    blur = cv2.blur(img, (7, 7))
```

#### 2. 锐化引入过多噪声
```python
# ❌ 错误做法：直接使用高强度锐化
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpened = cv2.filter2D(img, -1, kernel)

# ✅ 正确做法：先去噪再锐化
denoised = cv2.GaussianBlur(img, (3, 3), 0)
sharpened = cv2.filter2D(denoised, -1, kernel)

# 或者混合原图和锐化图
sharpened = cv2.addWeighted(img, 0.7, sharpened, 0.3, 0)
```

#### 3. Canny边缘检测阈值不当
```python
# ❌ 错误做法：硬编码阈值
edges = cv2.Canny(gray, 50, 150)

# ✅ 正确做法：根据图像自动计算
v = np.median(gray)
lower = int(max(0, 0.66 * v))
upper = int(min(255, 1.33 * v))
edges = cv2.Canny(gray, lower, upper)
```

#### 4. 双边滤波速度太慢
```python
# ❌ 错误做法：参数过大
bilateral = cv2.bilateralFilter(img, 25, 100, 100)  # 很慢

# ✅ 正确做法：先缩小图像再双边滤波
h, w = img.shape[:2]
small = cv2.resize(img, (w//2, h//2))
bilateral_small = cv2.bilateralFilter(small, 9, 75, 75)
bilateral = cv2.resize(bilateral_small, (w, h))
```

#### 5. Sobel梯度计算错误
```python
# ❌ 错误做法：直接使用有符号结果
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
cv2.imshow('Sobel', sobelx)  # 显示不正确

# ✅ 正确做法：取绝对值并转为uint8
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
sobelx = np.uint8(np.absolute(sobelx))
cv2.imshow('Sobel', sobelx)
```

---

## ❓ 常见问题

### Q1: 如何选择合适的滤波核大小？
**A:** 核大小的选择需要权衡：
- **3x3**: 轻微平滑，保留细节
- **5x5**: 中等平滑，常用
- **7x7及以上**: 强平滑，但模糊严重

**经验法则：**
```
核大小 ≈ 噪声颗粒大小 × 2 - 3
```

如果不确定，可以从5x5开始尝试。

### Q2: 高斯滤波的 sigma 参数如何设置？
**A:** sigma 参数控制高斯分布的标准差：

```python
# sigma = 0（推荐）
# OpenCV 自动根据核大小计算 sigma
blur = cv2.GaussianBlur(img, (5, 5), 0)

# 手动指定 sigma
blur = cv2.GaussianBlur(img, (5, 5), sigmaX=1.5)

# sigmaX 和 sigmaY 不同
blur = cv2.GaussianBlur(img, (5, 5), sigmaX=1.0, sigmaY=2.0)
```

**参考值：**
- sigma = 0.5-1.0: 轻微平滑
- sigma = 1.0-2.0: 中等平滑
- sigma > 2.0: 强平滑

### Q3: 为什么双边滤波很慢？
**A:** 双边滤波的时间复杂度是 O(N × k²)，其中：
- N 是图像像素数
- k 是滤波直径

**优化方法：**
1. 减小滤波直径 d
2. 先缩小图像处理，再放大回原尺寸
3. 使用近似算法（如域变换滤波）
4. 对感兴趣区域（ROI）处理，不是整图

### Q4: Canny的双阈值如何选择？
**A:** 双阈值包含：
- **低阈值**: 检测弱边缘
- **高阈值**: 检测强边缘

**推荐比例：** 高阈值 = 低阈值 × 2-3

**自动选择方法：**
```python
def auto_canny_threshold(image, sigma=0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    return lower, upper
```

**手动调整指南：**
- 低噪声: 50-150
- 中等噪声: 100-200
- 高噪声: 150-300

### Q5: 如何评估滤波效果？
**A:** 有两种评估方法：

**定量评估：**
```python
# PSNR（峰值信噪比）
def calculate_psnr(img1, img2):
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr

# SSIM（结构相似性）
from skimage.metrics import structural_similarity as ssim
ssim_value = ssim(img1, img2, multichannel=True)
```

**定性评估：**
- 视觉观察去噪效果
- 边缘保留程度
- 是否引入伪影

### Q6: 锐化核的元素和为什么要是1？
**A:** 这是为了保持图像的整体亮度：

```python
# 如果元素和不是1
kernel = np.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])
# 元素和 = 4，会使图像变亮

# 正确的锐化核
kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
# 元素和 = 1，保持亮度不变
```

### Q7: 如何去除混合噪声（高斯+椒盐）？
**A:** 推荐的组合方法：

```python
# 方法1: 先中值后高斯
denoised = cv2.medianBlur(noisy_img, 3)
denoised = cv2.GaussianBlur(denoised, (3, 3), 0)

# 方法2: 自适应混合
# 对每个像素判断噪声类型后选择滤波器

# 方法3: 非局部均值去噪（OpenCV内置）
denoised = cv2.fastNlMeansDenoisingColored(noisy_img, None, 10, 10, 7, 21)
```

### Q8: Sobel算子的 ksize 参数如何选择？
**A:** ksize 决定Sobel核的大小，可选值：1, 3, 5, 7

```python
# ksize=1 (最快，但不够平滑)
sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=1)

# ksize=3 (推荐，平衡速度和效果)
sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)

# ksize=5 (更平滑，但计算量大)
sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
```

**选择建议：**
- 实时应用: ksize=1 或 3
- 精确检测: ksize=3
- 高噪声图像: ksize=5

### Q9: 如何检测图像中的噪声类型？
**A:** 可以通过直方图分析：

```python
def detect_noise_type(img):
    """检测图像中的主要噪声类型"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 计算直方图
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    # 统计极值点（可能表示椒盐噪声）
    dark_pixels = np.sum(gray < 10)
    bright_pixels = np.sum(gray > 245)
    total_pixels = gray.size

    # 如果极值像素比例高，可能是椒盐噪声
    if (dark_pixels + bright_pixels) / total_pixels > 0.05:
        return "椒盐噪声（Salt-Pepper Noise）"

    # 分析直方图分布
    # 如果直方图呈现明显的高斯分布，可能是高斯噪声
    return "高斯噪声（Gaussian Noise）"

# 使用
noise_type = detect_noise_type(noisy_img)
print(f"检测到噪声类型: {noise_type}")
```

### Q10: 如何实时调整滤波参数？
**A:** 使用 OpenCV 的 Trackbar：

```python
def nothing(x):
    pass

# 创建窗口
cv2.namedWindow('Filter Control')

# 创建滑动条
cv2.createTrackbar('Kernel Size', 'Filter Control', 5, 20, nothing)
cv2.createTrackbar('Sigma', 'Filter Control', 0, 20, nothing)

while True:
    # 读取参数
    ksize = cv2.getTrackbarPos('Kernel Size', 'Filter Control')
    sigma = cv2.getTrackbarPos('Sigma', 'Filter Control')

    # 确保核大小为奇数
    if ksize % 2 == 0:
        ksize += 1

    # 应用滤波
    filtered = cv2.GaussianBlur(img, (ksize, ksize), sigma)

    # 显示结果
    cv2.imshow('Filter Control', filtered)

    # ESC键退出
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
```

---

## 📚 参考资料

### 官方文档
- [OpenCV 图像平滑](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)
- [OpenCV Canny 边缘检测](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [OpenCV 自定义滤波](https://docs.opencv.org/4.x/d4/dbd/tutorial_filter_2d.html)

### 项目文档
- [04-图像滤波与去噪](../../docs/04-图像滤波与去噪.md)
- [示例代码](../../src/examples/04-filtering-denoise.py)

### 扩展阅读
- [图像滤波算法详解](https://en.wikipedia.org/wiki/Kernel_(image_processing))
- [Canny边缘检测原理](https://en.wikipedia.org/wiki/Canny_edge_detector)
- [双边滤波论文](https://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf)

---

## 🎓 学习检查点

完成本任务后，你应该能够：
- [ ] 理解图像噪声的类型（高斯、椒盐）
- [ ] 掌握线性滤波（均值、高斯）
- [ ] 掌握非线性滤波（中值、双边）
- [ ] 理解卷积核的概念和设计
- [ ] 实现自定义锐化卷积核
- [ ] 掌握 Sobel 和 Canny 边缘检测
- [ ] 计算和解释 PSNR
- [ ] 根据场景选择合适的滤波方法
- [ ] 调优滤波参数
- [ ] 处理混合噪声

---

## 🚀 扩展挑战（可选）

完成基础任务后，可以尝试以下挑战：

### 挑战1：交互式滤波器（15分）
- 使用 Trackbar 实时调整所有滤波参数
- 支持切换不同滤波方法
- 实时预览滤波效果
- 显示 PSNR 和处理时间

### 挑战2：自动参数调优（20分）
- 实现自动噪声类型检测
- 根据噪声类型自动选择最佳滤波器
- 自动优化滤波参数（网格搜索）
- 输出最优参数组合

### 挑战3：高级去噪算法（25分）
- 实现非局部均值去噪（fastNlMeansDenoising）
- 实现维纳滤波
- 对比多种算法的效果
- 制作性能对比图表

### 挑战4：边缘检测优化（20分）
- 实现 Laplacian 边缘检测
- 实现 Scharr 算子
- 对比 Sobel、Scharr、Laplacian 效果
- 实现边缘连接和细化

### 挑战5：视频去噪（30分）
- 从摄像头读取视频
- 实时对视频帧进行去噪
- 实现时域滤波（结合前后帧）
- 展示去噪前后对比

---

**祝你好运！佛祖保佑，永无BUG！🙏**
