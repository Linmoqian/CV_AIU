# Task 3: 图像滤波与去噪

## 任务描述

使用不同的滤波方法对含噪图像进行去噪，并对比效果。

## 任务要求

### 1. 基础滤波（30分）
- 对含噪图像分别应用以下滤波方法：
  - 均值滤波（5x5核）
  - 高斯滤波（5x5核）
  - 中值滤波（5x5核）
  - 双边滤波

### 2. 效果对比（30分）
- 并排显示原图和滤波结果
- 分析每种滤波方法的优缺点
- 说明每种方法最适合的噪声类型

### 3. 自定义滤波核（20分）
- 创建一个3x3的锐化核
- 应用到模糊图像上
- 对比锐化前后的效果

### 4. 边缘检测（20分）
- 使用Sobel算子检测边缘
- 使用Canny算子检测边缘
- 对比两种方法的差异

## 提交要求

1. **代码文件**: `task3_solution.py`
2. **运行截图**: 显示所有滤波和边缘检测结果
3. **保存的图像**:
   - `filtering_mean.jpg`
   - `filtering_gaussian.jpg`
   - `filtering_median.jpg`
   - `filtering_bilateral.jpg`
   - `edges_sobel.jpg`
   - `edges_canny.jpg`
4. **分析报告**: 简要说明每种滤波方法的特点（50字以上）

## 评分标准

| 要求 | 分值 | 评分细则 |
|-----|------|---------|
| 基础滤波 | 30分 | 每种滤波方法7.5分 |
| 效果对比 | 30分 | 并排显示10分，分析说明20分 |
| 自定义滤波核 | 20分 | 锐化核定义正确10分，效果明显10分 |
| 边缘检测 | 20分 | Sobel和Canny各10分 |

## 提示

### 读取含噪图片
```python
img = cv2.imread('../assets/sample-images/noisy/noisy-gaussian.jpg')
# 或椒盐噪声
img = cv2.imread('../assets/sample-images/noisy/noisy-salt-pepper.jpg')
```

### 滤波方法
```python
# 均值滤波
blur_mean = cv2.blur(img, (5, 5))

# 高斯滤波
blur_gaussian = cv2.GaussianBlur(img, (5, 5), 0)

# 中值滤波
blur_median = cv2.medianBlur(img, 5)

# 双边滤波
blur_bilateral = cv2.bilateralFilter(img, 15, 80, 80)
```

### 并排显示
```python
import numpy as np

row1 = np.hstack([img, blur_mean, blur_gaussian])
row2 = np.hstack([blur_median, blur_bilateral, result])
result = np.vstack([row1, row2])
result = cv2.resize(result, None, fx=0.5, fy=0.5)
cv2.imshow('Comparison', result)
```

### 锐化核
```python
kernel_sharpen = np.array([
    [-1, -1, -1],
    [-1,  9, -1],
    [-1, -1, -1]
])

sharpened = cv2.filter2D(blur_img, -1, kernel_sharpen)
```

### 边缘检测
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Sobel
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobelx = np.uint8(np.absolute(sobelx))

# Canny
edges = cv2.Canny(gray, 50, 150)
```

## 分析报告模板

```markdown
# 图像滤波分析报告

## 1. 均值滤波
- 特点: 简单快速，但会模糊边缘
- 适用场景: 轻微高斯噪声
- 效果: [你的评价]

## 2. 高斯滤波
- 特点: 权重呈高斯分布，保留边缘较好
- 适用场景: 高斯噪声
- 效果: [你的评价]

## 3. 中值滤波
- 特点: 对椒盐噪声效果最好
- 适用场景: 椒盐噪声
- 效果: [你的评价]

## 4. 双边滤波
- 特点: 保留边缘的同时去噪
- 适用场景: 美颜、磨皮
- 效果: [你的评价]
```

## 扩展挑战（可选）

1. 尝试不同大小的核（3x3, 7x7, 9x9），对比效果
2. 对同一张图先后添加高斯噪声和椒盐噪声，测试哪种滤波效果最好
3. 实现交互式滤波器，可以实时调整参数

## 常见问题

**Q: 为什么中值滤波对椒盐噪声效果好？**
A: 中值滤波取中值，不受极值影响，能很好地去除黑白噪点

**Q: 双边滤波为什么慢？**
A: 需要同时计算空间距离和颜色差异，计算量大

**Q: Canny阈值如何选择？**
A: 低阈值用于弱边缘，高阈值用于强边缘，通常高阈值=低阈值×2-3
