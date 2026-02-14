# Task 1: 图像基本操作

## 📚 学习目标

通过完成本任务，你将掌握：
- ✅ OpenCV 图像读取和保存的基本方法
- ✅ 图像属性的查看和理解（尺寸、通道数、数据类型）
- ✅ 图像色彩空间转换（BGR ↔ 灰度）
- ✅ 图像缩放的多种方法
- ✅ 图像翻转操作
- ✅ 图像裁剪（ROI 选择）
- ✅ 图像旋转操作
- ✅ 中文路径问题的处理

## 🎯 任务概述

本任务要求你完成一系列图像基本操作，是学习 OpenCV 的基础。你将编写一个 Python 程序，对一张图片进行多种操作，并保存处理结果。

**预计时间：** 45-60 分钟
**难度：** ★★

## 📋 前置知识

在开始之前，确保你已经：
- [ ] 完成了 [00-环境搭建](../../docs/00-环境搭建.md)
- [ ] 阅读 [01-OpenCV简介与基础](../../docs/01-OpenCV简介与基础.md)
- [ ] 阅读 [02-图像基本操作](../../docs/02-图像基本操作.md)
- [ ] 运行过 `src/examples/01-read-display.py` 和 `02-basic-operations.py`

## 🔧 开发环境

```bash
# 确保已安装必要的库
pip install opencv-python numpy

# 测试图片位置
../../assets/sample-images/basic/landscape.jpg
```

## 📝 任务要求

### 1. 读取图像

**目标：** 正确读取一张彩色图片并显示其属性

**要求：**
- 使用 `cv2.imread()` 或中文路径兼容函数读取图片
- 检查图像是否成功读取（处理读取失败的情况）
- 打印以下信息：
  - 图像宽度、高度、通道数
  - 图像总像素数
  - 数据类型
  - 某个像素的 BGR 值

**提示：**
```python
import cv2
import numpy as np
import sys
import os

# 添加 utils 路径以支持中文路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

# 读取图片
img_path = get_image_path('sample-images/basic/landscape.jpg')
if img_path is None:
    print("错误：找不到图片！")
    exit()

img = imread_chinese(img_path)

# 检查是否成功
if img is None:
    print("错误：图片读取失败！")
    exit()

# 打印属性
height, width = img.shape[:2]
print(f"尺寸: {width} x {height}")
print(f"通道数: {img.shape[2] if len(img.shape) == 3 else 1}")
```

---

### 2. 转换为灰度图

**目标：** 将彩色图像转换为灰度图并对比显示

**要求：**
- 使用 `cv2.cvtColor()` 将 BGR 图像转换为灰度图
- 对比原图和灰度图，观察差异
- 保存灰度图为 `gray.jpg`

**核心代码：**
```python
# 方法1：使用 cvtColor
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 方法2：读取时直接转为灰度
# gray = imread_chinese(img_path, cv2.IMREAD_GRAYSCALE)

# 保存
cv2.imwrite('gray.jpg', gray)

# 对比显示（可选）
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2)
axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
axes[0].set_title('Original')
axes[1].imshow(gray, cmap='gray')
axes[1].set_title('Grayscale')
plt.show()
```

---

### 3. 图像缩放

**目标：** 掌握多种图像缩放方法

**要求：**
1. **缩小50%**
   - 使用 `cv2.resize()` 配合 `fx=0.5, fy=0.5`
   - 保存为 `resized_small.jpg`

2. **放大2倍**
   - 使用 `cv2.resize()` 配合 `fx=2.0, fy=2.0`
   - 注意：放大可能使用 `cv2.INTER_CUBIC` 插值
   - 保存为 `resized_large.jpg`

3. **指定宽度缩放**
   - 保持宽高比，将图像宽度缩放到 800 像素
   - 计算对应的高度

**核心代码：**
```python
height, width = img.shape[:2]

# 1. 缩小50%
small = cv2.resize(img, None, fx=0.5, fy=0.5,
                   interpolation=cv2.INTER_AREA)
cv2.imwrite('resized_small.jpg', small)

# 2. 放大2倍
large = cv2.resize(img, None, fx=2.0, fy=2.0,
                   interpolation=cv2.INTER_CUBIC)
cv2.imwrite('resized_large.jpg', large)

# 3. 指定宽度800，保持宽高比
new_width = 800
scale = new_width / width
new_height = int(height * scale)
resized = cv2.resize(img, (new_width, new_height))
```

---

### 4. 图像翻转

**目标：** 实现图像的水平、垂直和双向翻转

**要求：**
1. **水平翻转**（镜像效果）
   - 使用 `cv2.flip(img, 1)`
   - 保存为 `flipped_horizontal.jpg`

2. **垂直翻转**
   - 使用 `cv2.flip(img, 0)`
   - 保存为 `flipped_vertical.jpg`

3. **同时水平和垂直翻转**
   - 使用 `cv2.flip(img, -1)`
   - 保存为 `flipped_both.jpg`

**核心代码：**
```python
# 水平翻转
h_flip = cv2.flip(img, 1)
cv2.imwrite('flipped_horizontal.jpg', h_flip)

# 垂直翻转
v_flip = cv2.flip(img, 0)
cv2.imwrite('flipped_vertical.jpg', v_flip)

# 同时翻转
hv_flip = cv2.flip(img, -1)
cv2.imwrite('flipped_both.jpg', hv_flip)
```

---

### 5. 图像裁剪

**目标：** 裁剪图像的指定区域（ROI - Region of Interest）

**要求：**
- 裁剪图像的中心区域（原图尺寸的 1/4）
- 使用 NumPy 数组切片：`img[y1:y2, x1:x2]`
- 保存为 `cropped.jpg`

**核心代码：**
```python
h, w = img.shape[:2]

# 计算裁剪区域（中心1/4）
start_x, start_y = w // 4, h // 4
end_x, end_y = start_x * 3, start_y * 3

# 裁剪
cropped = img[start_y:end_y, start_x:end_x]
cv2.imwrite('cropped.jpg', cropped)

print(f"裁剪区域: ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
print(f"裁剪后尺寸: {cropped.shape[1]} x {cropped.shape[0]}")
```

---

### 6. 图像旋转

**目标：** 实现图像的90度、180度、270度旋转

**要求：**
- 使用 `cv2.rotate()` 旋转图像
- 保存三个旋转结果

**核心代码：**
```python
# 旋转90度顺时针
rot_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite('rotated_90.jpg', rot_90)

# 旋转180度
rot_180 = cv2.rotate(img, cv2.ROTATE_180)
cv2.imwrite('rotated_180.jpg', rot_180)

# 旋转270度（或90度逆时针）
rot_270 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
cv2.imwrite('rotated_270.jpg', rot_270)
```

---

## 📦 提交要求

### 必交内容

1. **代码文件**：`task1_solution.py`
   - 代码注释清晰
   - 包含适当的错误处理
   - 遵循 PEP 8 规范

2. **保存的图像**（按任务要求命名）：
   ```
   gray.jpg
   resized_small.jpg
   resized_large.jpg
   flipped_horizontal.jpg
   flipped_vertical.jpg
   flipped_both.jpg
   cropped.jpg
   ```

3. **运行结果截图**：`result_screenshot.png`
   - 显示程序运行的控制台输出
   - 可以包含图像显示窗口的截图

### 提交格式

```
task-01-submission/
├── task1_solution.py        # 你的代码
├── result_screenshot.png     # 运行结果截图
└── output_images/            # 输出图像文件夹
    ├── gray.jpg
    ├── resized_small.jpg
    ├── resized_large.jpg
    ├── flipped_horizontal.jpg
    ├── flipped_vertical.jpg
    ├── flipped_both.jpg
    └── cropped.jpg
```

---

## 💡 完整代码框架

```python
"""
Task 1: 图像基本操作
姓名：[你的名字]
学号：[你的学号]
日期：[提交日期]
"""

import cv2
import numpy as np
import sys
import os

# ==================== 配置区 ====================
# 添加 utils 路径以支持中文路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/utils'))
from io_helpers import imread_chinese, get_image_path

# 图片路径
IMG_PATH = 'sample-images/basic/landscape.jpg'
OUTPUT_DIR = 'output_images'

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 1. 读取图像 ====================
print("=" * 60)
print("Task 1: 图像基本操作")
print("=" * 60)

print("\n[1] 读取图像...")
img_path = get_image_path(IMG_PATH)
if img_path is None:
    print("  [ERROR] 找不到图片！")
    sys.exit(1)

img = imread_chinese(img_path)
if img is None:
    print("  [ERROR] 图片读取失败！")
    sys.exit(1)

height, width = img.shape[:2]
channels = img.shape[2] if len(img.shape) == 3 else 1

print(f"  [OK] 图片读取成功")
print(f"  - 尺寸: {width} x {height}")
print(f"  - 通道数: {channels}")
print(f"  - 总像素: {img.size}")
print(f"  - 数据类型: {img.dtype}")

# ==================== 2. 灰度转换 ====================
print("\n[2] 灰度转换...")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(f'{OUTPUT_DIR}/gray.jpg', gray)
print(f"  [OK] 灰度图已保存")

# ==================== 3. 图像缩放 ====================
print("\n[3] 图像缩放...")

# 缩小50%
small = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
cv2.imwrite(f'{OUTPUT_DIR}/resized_small.jpg', small)
print(f"  [OK] 缩小50%: {small.shape[1]} x {small.shape[0]}")

# 放大2倍
large = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
cv2.imwrite(f'{OUTPUT_DIR}/resized_large.jpg', large)
print(f"  [OK] 放大2倍: {large.shape[1]} x {large.shape[0]}")

# 指定宽度800
new_width = 800
scale = new_width / width
new_height = int(height * scale)
resized = cv2.resize(img, (new_width, new_height))
cv2.imwrite(f'{OUTPUT_DIR}/resized_800.jpg', resized)
print(f"  [OK] 宽度800: {resized.shape[1]} x {resized.shape[0]}")

# ==================== 4. 图像翻转 ====================
print("\n[4] 图像翻转...")

h_flip = cv2.flip(img, 1)
cv2.imwrite(f'{OUTPUT_DIR}/flipped_horizontal.jpg', h_flip)
print(f"  [OK] 水平翻转")

v_flip = cv2.flip(img, 0)
cv2.imwrite(f'{OUTPUT_DIR}/flipped_vertical.jpg', v_flip)
print(f"  [OK] 垂直翻转")

hv_flip = cv2.flip(img, -1)
cv2.imwrite(f'{OUTPUT_DIR}/flipped_both.jpg', hv_flip)
print(f"  [OK] 双向翻转")

# ==================== 5. 图像裁剪 ====================
print("\n[5] 图像裁剪...")

start_x, start_y = w // 4, h // 4
end_x, end_y = start_x * 3, start_y * 3

cropped = img[start_y:end_y, start_x:end_x]
cv2.imwrite(f'{OUTPUT_DIR}/cropped.jpg', cropped)
print(f"  [OK] 裁剪中心区域")
print(f"  - 裁剪区域: ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
print(f"  - 裁剪后尺寸: {cropped.shape[1]} x {cropped.shape[0]}")

# ==================== 6. 图像旋转 ====================
print("\n[6] 图像旋转...")

rot_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite(f'{OUTPUT_DIR}/rotated_90.jpg', rot_90)
print(f"  [OK] 旋转90度")

rot_180 = cv2.rotate(img, cv2.ROTATE_180)
cv2.imwrite(f'{OUTPUT_DIR}/rotated_180.jpg', rot_180)
print(f"  [OK] 旋转180度")

rot_270 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
cv2.imwrite(f'{OUTPUT_DIR}/rotated_270.jpg', rot_270)
print(f"  [OK] 旋转270度")

# ==================== 完成 ====================
print("\n" + "=" * 60)
print("所有操作完成！")
print(f"输出目录: {OUTPUT_DIR}/")
print("=" * 60)
```

---

## 🐛 调试技巧

### 常见错误及解决方法

#### 1. 图像读取失败
```python
# ❌ 错误做法
img = cv2.imread('包含中文的路径.jpg')

# ✅ 正确做法
from io_helpers import imread_chinese
img = imread_chinese('包含中文的路径.jpg')
```

#### 2. 裁剪坐标超出范围
```python
# ❌ 错误做法
crop = img[100:500, 100:500]  # 可能超出图像范围

# ✅ 正确做法
h, w = img.shape[:2]
y1, y2 = max(0, 100), min(h, 500)
x1, x2 = max(0, 100), min(w, 500)
crop = img[y1:y2, x1:x2]
```

#### 3. 缩放后图像失真
```python
# ❌ 错误做法
small = cv2.resize(img, None, fx=0.5)  # 默认插值可能不佳

# ✅ 正确做法
small = cv2.resize(img, None, fx=0.5, fy=0.5,
                   interpolation=cv2.INTER_AREA)  # 缩小用 AREA
large = cv2.resize(img, None, fx=2.0, fy=2.0,
                   interpolation=cv2.INTER_CUBIC)  # 放大用 CUBIC
```

---

## ❓ 常见问题

### Q1: 图像读取失败怎么办？
**A:** 检查以下几点：
1. 文件路径是否正确（使用相对或绝对路径）
2. 文件是否存在
3. 如果路径包含中文，使用 `imread_chinese()` 函数
4. 检查文件格式是否支持（.jpg, .png, .bmp等）

### Q2: 缩放后图像失真严重？
**A:** 尝试不同的插值方法：
- `cv2.INTER_NEAREST` - 最近邻（最快，质量最差）
- `cv2.INTER_LINEAR` - 双线性（默认）
- `cv2.INTER_CUBIC` - 双三次（质量好，适合放大）
- `cv2.INTER_AREA` - 区域插值（适合缩小）

### Q3: 裁剪坐标超出范围导致错误？
**A:** 使用 `min)` 限制坐标：
```python
h, w = img.shape[:2]
y1, y2 = max(0, start_y), min(h, end_y)
x1, x2 = max(0, start_x), min(w, end_x)
```

### Q4: 如何保持宽高比缩放？
**A:** 计算缩放比例：
```python
target_width = 800
scale = target_width / img.shape[1]
target_height = int(img.shape[0] * scale)
resized = cv2.resize(img, (target_width, target_height))
```

### Q5: 保存的图像质量很差？
**A:** 对于 JPEG 格式，可以指定质量：
```python
cv2.imwrite('output.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])
```

---

## 📚 参考资料

- [OpenCV Python 教程 - 图像基本操作](https://docs.opencv.org/4.x/dd/d49/tutorial_py_corner_sharpness.html)
- [示例代码](../../src/examples/02-basic-operations.py)
- [工具函数](../../src/utils/)

---

## 🎓 学习检查点

完成本任务后，你应该能够：
- [ ] 熟练使用 `cv2.imread()` 读取图像
- [ ] 理解图像的 shape、size、dtype 属性
- [ ] 掌握 `cv2.cvtColor()` 进行色彩空间转换
- [ ] 熟练使用 `cv2.resize()` 进行图像缩放
- [ ] 掌握 `cv2.flip()` 进行图像翻转
- [ ] 使用 NumPy 切片进行图像裁剪
- [ ] 使用 `cv2.rotate()` 进行图像旋转
- [ ] 处理中文路径问题

---

**祝你好运！佛祖保佑，永无BUG！🙏**
