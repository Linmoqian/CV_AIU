# Task 2: 色彩空间转换与颜色提取

## 📚 学习目标

通过完成本任务,你将掌握：
- ✅ 理解不同的色彩空间（BGR、RGB、HSV、灰度）
- ✅ 掌握色彩空间之间的转换方法
- ✅ 理解 HSV 色彩空间的三个分量（色调、饱和度、明度）
- ✅ 掌握使用 `cv2.inRange()` 创建颜色掩膜
- ✅ 掌握按位运算操作（AND、OR、NOT、XOR）
- ✅ 实现红、绿、蓝、黄四种颜色的提取
- ✅ 编写通用的颜色识别函数
- ✅ 应用形态学操作去除噪声

## 🎯 任务概述

本任务要求你使用 HSV 色彩空间从图像中提取特定颜色的物体。HSV 色彩空间比 RGB 更适合颜色识别，因为它将颜色信息（色调 H）与强度信息（饱和度 S、明度 V）分离。你将完成从 BGR 到 HSV 的转换，分离并显示三个通道，实现红色提取，并编写一个通用的颜色识别函数。

**预计时间：** 60-90 分钟
**难度：** ★★★

## 📋 前置知识

在开始之前，确保你已经：
- [ ] 完成了 [Task 1: 图像基本操作](../task-01/README.md)
- [ ] 阅读 [03-色彩空间与颜色提取](../../docs/03-色彩空间与颜色提取.md)
- [ ] 理解 NumPy 数组的基本操作
- [ ] 理解图像的掩膜（Mask）概念

## 🔧 开发环境

```bash
# 确保已安装必要的库
pip install opencv-python numpy matplotlib

# 测试图片位置
../../assets/sample-images/colors/
```

**推荐测试图像：**
- `fruits.jpg` - 包含多种颜色的水果
- `traffic-lights.jpg` - 交通灯
- `colorful-objects.jpg` - 彩色物体
- 或自行拍摄包含明显颜色的图片

## 📝 任务要求

### 1. 色彩空间转换与通道分离

**目标：** 将 BGR 图像转换为 HSV，并分离显示三个通道

**要求：**
1. **BGR 到 HSV 转换**
   - 使用 `cv2.cvtColor(img, cv2.COLOR_BGR2HSV)`
   - 理解 HSV 的取值范围：H(0-180), S(0-255), V(0-255)

2. **通道分离**
   - 使用 `cv2.split()` 或 NumPy 索引分离 H、S、V 通道
   - 将三个通道并排显示为一张图像
   - 保存为 `hsv_channels.jpg`

3. **理解各通道含义**
   - H（Hue，色调）：颜色类型（0-180）
   - S（Saturation，饱和度）：颜色纯度（0-255）
   - V（Value，明度）：亮度（0-255）

**核心代码：**
```python
import cv2
import numpy as np

# 1. 转换为 HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 2. 分离通道
h, s, v = cv2.split(hsv)

# 或者使用 NumPy 索引
# h = hsv[:, :, 0]
# s = hsv[:, :, 1]
# v = hsv[:, :, 2]

# 3. 显示各通道（需要归一化到 0-255 用于显示）
h_show = cv2.normalize(h, None, 0, 255, cv2.NORM_MINMAX)
s_show = cv2.normalize(s, None, 0, 255, cv2.NORM_MINMAX)
v_show = v

# 4. 合并为一张图（三个通道并排）
hsv_channels = np.hstack((h_show, s_show, v_show))
cv2.imwrite('hsv_channels.jpg', hsv_channels)

# 打印各通道的值范围
print(f"H通道范围: {h.min)
print(f"S通道范围: {s.min)
print(f"V通道范围: {v.min)
```

**提示：**
- H 通道在 OpenCV 中范围是 0-180（通常是 0-360 的一半）
- S 和 V 通道范围是 0-255
- 显示时需要将 H 通道归一化到 0-255 才能正确显示

---

### 2. 红色提取

**目标：** 从图像中提取所有红色区域并显示

**要求：**
1. **定义红色 HSV 范围**
   - 红色在 HSV 空间跨越 0 和 180（色环两端）
   - 需要定义两个范围并合并

2. **创建掩膜**
   - 使用 `cv2.inRange()` 创建两个掩膜
   - 使用 `cv2.bitwise_or()` 合并掩膜
   - 应用形态学操作去除噪声

3. **提取并显示结果**
   - 使用 `cv2.bitwise_and()` 提取红色区域
   - 保存掩膜为 `red_mask.jpg`
   - 保存提取结果为 `red_extracted.jpg`

**核心代码：**
```python
# 定义红色的两个范围
lower_red1 = np.array([0, 100, 100])    # 下限1
upper_red1 = np.array([10, 255, 255])   # 上限1

lower_red2 = np.array([170, 100, 100])  # 下限2
upper_red2 = np.array([180, 255, 255])  # 上限2

# 创建两个掩膜
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

# 合并掩膜
mask = cv2.bitwise_or(mask1, mask2)

# 形态学操作去除噪声
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 开运算去除小白点
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # 闭运算填充小黑洞

# 应用掩膜提取红色
result = cv2.bitwise_and(img, img, mask=mask)

# 保存结果
cv2.imwrite('red_mask.jpg', mask)
cv2.imwrite('red_extracted.jpg', result)
```

**提示：**
- 红色特殊，因为它在色环的起始和结束位置
- 如果提取效果不好，可以调整 S 和 V 的范围（100-255 是经验值）
- 形态学操作可以有效去除噪声

---

### 3. 其他颜色提取

**目标：** 实现绿、蓝、黄三种颜色的提取

**要求：**
1. **绿色提取**
   - HSV 范围：H(35-85), S(100-255), V(100-255)
   - 保存为 `green_mask.jpg` 和 `green_extracted.jpg`

2. **蓝色提取**
   - HSV 范围：H(85-135), S(100-255), V(100-255)
   - 保存为 `blue_mask.jpg` 和 `blue_extracted.jpg`

3. **黄色提取**
   - HSV 范围：H(20-35), S(100-255), V(100-255)
   - 保存为 `yellow_mask.jpg` 和 `yellow_extracted.jpg`

**核心代码：**
```python
# 定义颜色范围字典
COLOR_RANGES = {
    'green': {
        'lower': np.array([35, 100, 100]),
        'upper': np.array([85, 255, 255])
    },
    'blue': {
        'lower': np.array([85, 100, 100]),
        'upper': np.array([135, 255, 255])
    },
    'yellow': {
        'lower': np.array([20, 100, 100]),
        'upper': np.array([35, 255, 255])
    }
}

# 提取绿色
lower_green = COLOR_RANGES['green']['lower']
upper_green = COLOR_RANGES['green']['upper']
green_mask = cv2.inRange(hsv, lower_green, upper_green)
green_result = cv2.bitwise_and(img, img, mask=green_mask)
cv2.imwrite('green_mask.jpg', green_mask)
cv2.imwrite('green_extracted.jpg', green_result)

# 提取蓝色
lower_blue = COLOR_RANGES['blue']['lower']
upper_blue = COLOR_RANGES['blue']['upper']
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
blue_result = cv2.bitwise_and(img, img, mask=blue_mask)
cv2.imwrite('blue_mask.jpg', blue_mask)
cv2.imwrite('blue_extracted.jpg', blue_result)

# 提取黄色
lower_yellow = COLOR_RANGES['yellow']['lower']
upper_yellow = COLOR_RANGES['yellow']['upper']
yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
yellow_result = cv2.bitwise_and(img, img, mask=yellow_mask)
cv2.imwrite('yellow_mask.jpg', yellow_mask)
cv2.imwrite('yellow_extracted.jpg', yellow_result)
```

**提示：**
- 不同颜色的 HSV 范围可能有重叠，这是正常的
- 如果提取不准确，可以适当放宽或缩紧范围
- 绿色和黄色在色环上相邻，容易混淆

---

### 4. 通用颜色识别函数

**目标：** 编写一个通用的函数，可以提取任意指定颜色

**要求：**
1. **函数签名**
   ```python
   def extract_color(img, color_name, show_result=True):
       """
       从图像中提取指定颜色

       参数:
           img: 输入图像（BGR格式）
           color_name: 颜色名称 ('red', 'green', 'blue', 'yellow')
           show_result: 是否显示结果（默认True）

       返回:
           mask: 二值掩膜（白色=目标颜色，黑色=其他）
           result: 提取结果图像
       """
   ```

2. **功能实现**
   - 内置四种颜色的 HSV 范围
   - 自动处理红色的特殊情况（两个范围）
   - 支持形态学去噪（可选）
   - 支持显示和保存结果

3. **错误处理**
   - 处理不支持的颜色的输入
   - 处理图像为 None 的情况

**完整代码框架：**
```python
def extract_color(img, color_name, show_result=True, morph_op=True):
    """
    从图像中提取指定颜色

    参数:
        img: 输入图像（BGR格式）
        color_name: 颜色名称 ('red', 'green', 'blue', 'yellow')
        show_result: 是否显示结果（默认True）
        morph_op: 是否应用形态学操作（默认True）

    返回:
        mask: 二值掩膜（白色=目标颜色，黑色=其他）
        result: 提取结果图像
    """
    # 检查图像
    if img is None:
        print("[ERROR] 输入图像为空！")
        return None, None

    # 定义颜色范围
    color_ranges = {
        'red': [
            (np.array([0, 100, 100]), np.array([10, 255, 255])),
            (np.array([170, 100, 100]), np.array([180, 255, 255]))
        ],
        'green': [
            (np.array([35, 100, 100]), np.array([85, 255, 255]))
        ],
        'blue': [
            (np.array([85, 100, 100]), np.array([135, 255, 255]))
        ],
        'yellow': [
            (np.array([20, 100, 100]), np.array([35, 255, 255]))
        ]
    }

    # 检查颜色名称
    color_name = color_name.lower()
    if color_name not in color_ranges:
        print(f"[ERROR] 不支持的颜色：{color_name}")
        print(f"支持的颜色：{list(color_ranges.keys)
        return None, None

    # 转换为 HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 创建掩膜
    ranges = color_ranges[color_name]
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

    for lower, upper in ranges:
        temp_mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.bitwise_or(mask, temp_mask)

    # 形态学操作（可选）
    if morph_op:
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 应用掩膜
    result = cv2.bitwise_and(img, img, mask=mask)

    # 显示结果
    if show_result:
        # 创建对比图
        contrast = np.hstack((img, result))
        cv2.imshow(f'Color Extraction: {color_name}', contrast)
        cv2.imshow(f'Mask: {color_name}', mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return mask, result

# 使用示例
if __name__ == "__main__":
    # 读取图像
    img = cv2.imread('test_image.jpg')

    # 提取红色
    mask, result = extract_color(img, 'red', show_result=True)
    cv2.imwrite('red_extracted.jpg', result)

    # 提取绿色
    mask, result = extract_color(img, 'green', show_result=False)
    cv2.imwrite('green_extracted.jpg', result)

    # 提取蓝色
    mask, result = extract_color(img, 'blue', show_result=False)
    cv2.imwrite('blue_extracted.jpg', result)

    # 提取黄色
    mask, result = extract_color(img, 'yellow', show_result=False)
    cv2.imwrite('yellow_extracted.jpg', result)
```

**提示：**
- 函数应该有清晰的文档字符串
- 返回的掩膜可以用于后续处理（如统计像素数、查找轮廓等）
- 形态学操作参数可以设为可选参数，增加灵活性

---

## 📦 提交要求

### 必交内容

1. **代码文件**：`task2_solution.py`
   - 包含所有四个任务的实现
   - 代码注释清晰，符合 PEP 8 规范
   - 包含通用的颜色提取函数

2. **保存的图像**（按任务要求命名）：
   ```
   hsv_channels.jpg          # H、S、V三通道并排显示
   red_mask.jpg              # 红色掩膜
   red_extracted.jpg         # 红色提取结果
   green_mask.jpg            # 绿色掩膜
   green_extracted.jpg       # 绿色提取结果
   blue_mask.jpg             # 蓝色掩膜
   blue_extracted.jpg        # 蓝色提取结果
   yellow_mask.jpg           # 黄色掩膜
   yellow_extracted.jpg      # 黄色提取结果
   ```

3. **运行结果截图**：`result_screenshot.png`
   - 显示程序运行的控制台输出
   - 可以包含图像显示窗口的截图

4. **实验报告**（可选，）：
   - 总结 HSV 色彩空间的特点
   - 分析不同颜色的提取效果
   - 讨论遇到的问题和解决方案

### 提交格式

```
task-02-submission/
├── task2_solution.py          # 你的代码
├── result_screenshot.png      # 运行结果截图
├── output_images/              # 输出图像文件夹
│   ├── hsv_channels.jpg
│   ├── red_mask.jpg
│   ├── red_extracted.jpg
│   ├── green_mask.jpg
│   ├── green_extracted.jpg
│   ├── blue_mask.jpg
│   ├── blue_extracted.jpg
│   ├── yellow_mask.jpg
│   └── yellow_extracted.jpg
└── report.md                   # 实验报告（可选）
```

---

## 💡 完整代码框架

```python
"""
Task 2: 色彩空间转换与颜色提取
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
IMG_PATH = 'sample-images/colors/fruits.jpg'
OUTPUT_DIR = 'output_images'

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 通用函数 ====================
def extract_color(img, color_name, show_result=False, morph_op=True):
    """
    从图像中提取指定颜色

    参数:
        img: 输入图像（BGR格式）
        color_name: 颜色名称 ('red', 'green', 'blue', 'yellow')
        show_result: 是否显示结果（默认False）
        morph_op: 是否应用形态学操作（默认True）

    返回:
        mask: 二值掩膜（白色=目标颜色，黑色=其他）
        result: 提取结果图像
    """
    # 检查图像
    if img is None:
        print("[ERROR] 输入图像为空！")
        return None, None

    # 定义颜色范围
    color_ranges = {
        'red': [
            (np.array([0, 100, 100]), np.array([10, 255, 255])),
            (np.array([170, 100, 100]), np.array([180, 255, 255]))
        ],
        'green': [
            (np.array([35, 100, 100]), np.array([85, 255, 255]))
        ],
        'blue': [
            (np.array([85, 100, 100]), np.array([135, 255, 255]))
        ],
        'yellow': [
            (np.array([20, 100, 100]), np.array([35, 255, 255]))
        ]
    }

    # 检查颜色名称
    color_name = color_name.lower()
    if color_name not in color_ranges:
        print(f"[ERROR] 不支持的颜色：{color_name}")
        print(f"支持的颜色：{list(color_ranges.keys)
        return None, None

    # 转换为 HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 创建掩膜
    ranges = color_ranges[color_name]
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

    for lower, upper in ranges:
        temp_mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.bitwise_or(mask, temp_mask)

    # 形态学操作（可选）
    if morph_op:
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 应用掩膜
    result = cv2.bitwise_and(img, img, mask=mask)

    # 显示结果
    if show_result:
        # 创建对比图
        contrast = np.hstack((img, result))
        cv2.imshow(f'Color Extraction: {color_name}', contrast)
        cv2.imshow(f'Mask: {color_name}', mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return mask, result

# ==================== 主程序 ====================
print("=" * 60)
print("Task 2: 色彩空间转换与颜色提取")
print("=" * 60)

# 1. 读取图像
print("\n[1] 读取图像...")
img_path = get_image_path(IMG_PATH)
if img_path is None:
    print("  [ERROR] 找不到图片！")
    sys.exit(1)

img = imread_chinese(img_path)
if img is None:
    print("  [ERROR] 图片读取失败！")
    sys.exit(1)

print(f"  [OK] 图片读取成功: {img.shape}")

# 2. 色彩空间转换与通道分离
print("\n[2] 色彩空间转换（BGR -> HSV）...")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)

print(f"  [OK] HSV 转换完成")
print(f"  - H通道范围: [{h.min)
print(f"  - S通道范围: [{s.min)
print(f"  - V通道范围: [{v.min)

# 归一化并合并显示
h_show = cv2.normalize(h, None, 0, 255, cv2.NORM_MINMAX)
hsv_channels = np.hstack((h_show, s, v))
cv2.imwrite(f'{OUTPUT_DIR}/hsv_channels.jpg', hsv_channels)
print(f"  [OK] HSV通道图已保存")

# 3. 红色提取
print("\n[3] 红色提取...")
red_mask, red_result = extract_color(img, 'red', show_result=False)
if red_mask is not None:
    cv2.imwrite(f'{OUTPUT_DIR}/red_mask.jpg', red_mask)
    cv2.imwrite(f'{OUTPUT_DIR}/red_extracted.jpg', red_result)
    red_pixels = cv2.countNonZero(red_mask)
    print(f"  [OK] 红色提取完成，检测到 {red_pixels} 个像素")

# 4. 绿色提取
print("\n[4] 绿色提取...")
green_mask, green_result = extract_color(img, 'green', show_result=False)
if green_mask is not None:
    cv2.imwrite(f'{OUTPUT_DIR}/green_mask.jpg', green_mask)
    cv2.imwrite(f'{OUTPUT_DIR}/green_extracted.jpg', green_result)
    green_pixels = cv2.countNonZero(green_mask)
    print(f"  [OK] 绿色提取完成，检测到 {green_pixels} 个像素")

# 5. 蓝色提取
print("\n[5] 蓝色提取...")
blue_mask, blue_result = extract_color(img, 'blue', show_result=False)
if blue_mask is not None:
    cv2.imwrite(f'{OUTPUT_DIR}/blue_mask.jpg', blue_mask)
    cv2.imwrite(f'{OUTPUT_DIR}/blue_extracted.jpg', blue_result)
    blue_pixels = cv2.countNonZero(blue_mask)
    print(f"  [OK] 蓝色提取完成，检测到 {blue_pixels} 个像素")

# 6. 黄色提取
print("\n[6] 黄色提取...")
yellow_mask, yellow_result = extract_color(img, 'yellow', show_result=False)
if yellow_mask is not None:
    cv2.imwrite(f'{OUTPUT_DIR}/yellow_mask.jpg', yellow_mask)
    cv2.imwrite(f'{OUTPUT_DIR}/yellow_extracted.jpg', yellow_result)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    print(f"  [OK] 黄色提取完成，检测到 {yellow_pixels} 个像素")

# 7. 统计颜色分布
print("\n[7] 颜色分布统计...")
total_pixels = img.shape[0] * img.shape[1]
print(f"  - 红色占比: {red_pixels/total_pixels*100:.2f}%")
print(f"  - 绿色占比: {green_pixels/total_pixels*100:.2f}%")
print(f"  - 蓝色占比: {blue_pixels/total_pixels*100:.2f}%")
print(f"  - 黄色占比: {yellow_pixels/total_pixels*100:.2f}%")

# ==================== 完成 ====================
print("\n" + "=" * 60)
print("所有操作完成！")
print(f"输出目录: {OUTPUT_DIR}/")
print("=" * 60)
```

---

## 🐛 调试技巧

### 常见错误及解决方法

#### 1. 颜色提取不准确
```python
# ❌ 错误做法：范围太窄
lower_red = np.array([0, 200, 200])  # S和V范围太高
upper_red = np.array([10, 255, 255])

# ✅ 正确做法：适当放宽范围
lower_red = np.array([0, 100, 100])  # S和V范围适中
upper_red = np.array([10, 255, 255])

# 如果还是不准，可以进一步放宽
lower_red = np.array([0, 50, 50])    # 更宽松的范围
upper_red = np.array([10, 255, 255])
```

#### 2. 红色提取效果差
```python
# ❌ 错误做法：只用一个范围
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
mask = cv2.inRange(hsv, lower_red, upper_red)

# ✅ 正确做法：使用两个范围并合并
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)
```

#### 3. 掩膜有很多噪声
```python
# ❌ 错误做法：直接使用掩膜
mask = cv2.inRange(hsv, lower, upper)
result = cv2.bitwise_and(img, img, mask=mask)

# ✅ 正确做法：应用形态学操作
mask = cv2.inRange(hsv, lower, upper)
kernel = np.ones((5, 5), np.uint8)
# 开运算：去除小的白色噪声
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
# 闭运算：填充小的黑色空洞
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
result = cv2.bitwise_and(img, img, mask=mask)
```

#### 4. HSV 通道显示不正确
```python
# ❌ 错误做法：直接显示
h, s, v = cv2.split(hsv)
cv2.imshow('H', h)  # H通道显示为黑色（范围0-180）

# ✅ 正确做法：归一化到0-255
h, s, v = cv2.split(hsv)
h_normalized = cv2.normalize(h, None, 0, 255, cv2.NORM_MINMAX)
cv2.imshow('H', h_normalized)
cv2.imshow('S', s)
cv2.imshow('V', v)
```

#### 5. 图像路径错误
```python
# ❌ 错误做法：硬编码路径
img = cv2.imread('D:/项目/CV培训/assets/sample-images/colors/fruits.jpg')

# ✅ 正确做法：使用辅助函数
from io_helpers import imread_chinese, get_image_path
img_path = get_image_path('sample-images/colors/fruits.jpg')
img = imread_chinese(img_path)
```

---

## ❓ 常见问题

### Q1: 为什么 HSV 更适合颜色识别？
**A:** RGB 色彩空间中，三个通道（R、G、B）都包含亮度信息，光照变化会影响所有通道，导致颜色识别不稳定。而 HSV 色彩空间将：
- **H（Hue，色调）**：只表示颜色类型（0-180）
- **S（Saturation，饱和度）**：表示颜色纯度
- **V（Value，明度）**：表示亮度

这样我们可以只关注 H 通道来识别颜色，S 和 V 用于过滤不合适的区域（如太暗或太淡的颜色）。

### Q2: 如何确定某个颜色的 HSV 范围？
**A:** 有几种方法：

**方法1：参考经验值**
```python
# 常见颜色的 HSV 范围（OpenCV中H范围是0-180）
红色：H(0-10 或 170-180), S(100-255), V(100-255)
绿色：H(35-85), S(100-255), V(100-255)
蓝色：H(85-135), S(100-255), V(100-255)
黄色：H(20-35), S(100-255), V(100-255)
橙色：H(10-20), S(100-255), V(100-255)
紫色：H(135-170), S(100-255), V(100-255)
```

**方法2：使用颜色选择器工具**
```python
# 创建一个简单的HSV调试器
def nothing(x):
    pass

cv2.namedWindow('HSV Trackbar')

# 创建滑动条
cv2.createTrackbar('H Low', 'HSV Trackbar', 0, 180, nothing)
cv2.createTrackbar('H High', 'HSV Trackbar', 180, 180, nothing)
cv2.createTrackbar('S Low', 'HSV Trackbar', 0, 255, nothing)
cv2.createTrackbar('S High', 'HSV Trackbar', 255, 255, nothing)
cv2.createTrackbar('V Low', 'HSV Trackbar', 0, 255, nothing)
cv2.createTrackbar('V High', 'HSV Trackbar', 255, 255, nothing)

while True:
    h_low = cv2.getTrackbarPos('H Low', 'HSV Trackbar')
    h_high = cv2.getTrackbarPos('H High', 'HSV Trackbar')
    s_low = cv2.getTrackbarPos('S Low', 'HSV Trackbar')
    s_high = cv2.getTrackbarPos('S High', 'HSV Trackbar')
    v_low = cv2.getTrackbarPos('V Low', 'HSV Trackbar')
    v_high = cv2.getTrackbarPos('V High', 'HSV Trackbar')

    lower = np.array([h_low, s_low, v_low])
    upper = np.array([h_high, s_high, v_high])

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC键退出
        break
```

**方法3：点击图像获取HSV值**
```python
def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        pixel = hsv[y, x]
        print(f"HSV值: H={pixel[0]}, S={pixel[1]}, V={pixel[2]}")

cv2.imshow('image', img)
cv2.setMouseCallback('image', get_hsv_value)
cv2.waitKey(0)
```

### Q3: 为什么红色需要两个范围？
**A:** 在 HSV 色彩空间中，色调（H）表示为色环上的角度：
- 红色在色环的起始位置（0°）和结束位置（360°）
- 在 OpenCV 中，H 的范围是 0-180（对应 0-360°）
- 因此红色跨越了 0 和 180 两个端点
- 需要定义两个范围：[0-10] 和 [170-180]，然后合并

### Q4: 形态学操作的作用是什么？
**A:** 形态学操作用于去除掩膜中的噪声：

**开运算（MORPH_OPEN）：先腐蚀后膨胀**
- 作用：去除小的白色噪声点
- 适用：掩膜中有孤立的小白点

**闭运算（MORPH_CLOSE）：先膨胀后腐蚀**
- 作用：填充小的黑色空洞
- 适用：掩膜中的目标区域有小黑洞

```python
kernel = np.ones((5, 5), np.uint8)

# 开运算：去噪
mask_clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# 闭运算：填充
mask_filled = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)
```

### Q5: 如何统计某种颜色的像素数量？
**A:** 使用 `cv2.countNonZero()`：
```python
# 统计掩膜中白色像素的数量（即提取到的颜色像素）
color_pixels = cv2.countNonZero(mask)

# 计算占比
total_pixels = img.shape[0] * img.shape[1]
percentage = (color_pixels / total_pixels) * 100

print(f"颜色像素数: {color_pixels}")
print(f"占比: {percentage:.2f}%")
```

### Q6: 如何同时提取多种颜色？
**A:** 在一张图上标记不同颜色：
```python
# 创建空白图像用于标记
marked = img.copy()

# 定义颜色和对应的BGR值
colors = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255)
}

for color_name, bgr_color in colors.items():
    mask, _ = extract_color(img, color_name, show_result=False)
    if mask is not None:
        # 在原图上用对应颜色标记
        marked[mask > 0] = bgr_color

cv2.imwrite('multi_color_marked.jpg', marked)
```

### Q7: 光照不均匀时如何处理？
**A:** 光照不均匀会影响颜色提取，可以尝试：

**方法1：放宽S和V的范围**
```python
lower = np.array([35, 50, 50])    # 降低S和V的下限
upper = np.array([85, 255, 255])
```

**方法2：使用自适应阈值**
```python
# 对V通道进行自适应阈值处理
v_channel = hsv[:, :, 2]
adaptive_v = cv2.adaptiveThreshold(
    v_channel, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)
```

**方法3：使用直方图均衡化**
```python
# 对V通道进行直方图均衡化
h, s, v = cv2.split(hsv)
v_eq = cv2.equalizeHist(v)
hsv_eq = cv2.merge([h, s, v_eq])
```

---

## 📚 参考资料

### 官方文档
- [OpenCV Python 教程 - 颜色追踪](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)
- [cv2.cvtColor 色彩空间转换](https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html)
- [cv2.inRange 颜色阈值](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga48af0ab51e36436c5d04340e036ce981)

### 项目文档
- [03-色彩空间与颜色提取](../../docs/03-色彩空间与颜色提取.md)
- [示例代码](../../src/examples/03-color-detection.py)
- [工具函数](../../src/utils/)

### 扩展阅读
- [HSV 色彩空间详解](https://zh.wikipedia.org/wiki/HSL和HSV色彩空间)
- [图像形态学操作](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)

---

## 🎓 学习检查点

完成本任务后，你应该能够：
- [ ] 理解 BGR、RGB、HSV 三种色彩空间的区别
- [ ] 熟练使用 `cv2.cvtColor()` 进行色彩空间转换
- [ ] 理解 HSV 三个通道（H、S、V）的物理意义
- [ ] 掌握 `cv2.inRange()` 创建颜色掩膜
- [ ] 掌握按位运算（AND、OR、NOT、XOR）
- [ ] 理解红色在 HSV 空间的特殊性
- [ ] 应用形态学操作去除掩膜噪声
- [ ] 编写通用的颜色识别函数
- [ ] 调试和优化颜色提取效果
- [ ] 处理光照不均匀的情况

---

## 🚀 扩展挑战（可选）

完成基础任务后，可以尝试以下挑战：

### 挑战1：交互式颜色选择器
- 使用 OpenCV 的滑动条（Trackbar）实时调整 HSV 范围
- 点击图像显示该点的 HSV 值
- 实时预览提取效果

### 挑战2：多目标追踪
- 同时提取图像中的多种颜色
- 统计每种颜色的像素数量和占比
- 在原图上用边界框标记不同颜色的物体

### 挑战3：光照鲁棒性
- 实现自适应的颜色提取
- 使用直方图均衡化处理光照变化
- 在不同光照条件下测试算法稳定性

### 挑战4：视频颜色检测
- 从摄像头实时读取视频
- 实时检测并追踪特定颜色的物体
- 显示颜色追踪的轨迹

---

**祝你好运！佛祖保佑，永无BUG！🙏**
