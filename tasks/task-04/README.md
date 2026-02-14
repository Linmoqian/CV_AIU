# Task 4: 边缘检测与形状计数

## 任务描述

使用边缘检测和霍夫变换检测图像中的硬币并计数。

## 任务要求

### 1. Canny边缘检测（30分）
- 读取coins.jpg图像
- 转灰度并高斯滤波
- 使用Canny检测边缘
- 尝试不同阈值，找到最佳参数

### 2. 霍夫圆变换（40分）
- 使用霍夫圆变换检测圆形
- 调整参数以准确检测所有硬币
- 绘制检测到的圆
- 统计硬币数量

### 3. 形状检测（30分）
- 查找边缘轮廓
- 根据面积和形状特征筛选圆形
- 在原图上标注检测到的硬币
- 显示计数结果

## 提交要求

1. **代码文件**: `task4_solution.py`
2. **运行截图**: 显示检测过程和结果
3. **保存的图像**:
   - `edges_canny.jpg`
   - `circles_detected.jpg`
   - `contours_detected.jpg`
4. **统计数据**: 打印检测到的硬币数量和位置

## 评分标准

| 要求 | 分值 | 评分细则 |
|-----|------|---------|
| Canny边缘检测 | 30分 | 参数合理15分，边缘清晰15分 |
| 霍夫圆变换 | 40分 | 检测准确20分，参数调优20分 |
| 形状检测 | 30分 | 轮廓查找15分，筛选准确15分 |

## 提示

### Canny边缘检测
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 自动阈值
median = np.median(blur)
lower = int(max(0, 0.7 * median))
upper = int(min(255, 1.3 * median))
edges = cv2.Canny(blur, lower, upper)

# 或手动阈值
edges = cv2.Canny(blur, 50, 150)
```

### 霍夫圆变换
```python
circles = cv2.HoughCircles(
    blur,              # 输入图像（灰度）
    cv2.HOUGH_GRADIENT,  # 方法
    dp=1,              # 累加器分辨率
    minDist=50,        # 圆心之间的最小距离
    param1=50,         # Canny高阈值
    param2=30,         # 检测阈值（越小检测到的圆越多）
    minRadius=20,      # 最小半径
    maxRadius=100      # 最大半径
)

if circles is not None:
    circles = np.round(circles[0, :]).astype("int")

    for (x, y, r) in circles:
        # 绘制圆
        cv2.circle(img, (x, y), r, (0, 255, 0), 2)
        # 绘制圆心
        cv2.circle(img, (x, y), 3, (0, 0, 255), -3)

    print(f"检测到 {len(circles)} 个硬币")
```

### 轮廓检测
```python
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

count = 0
for contour in contours:
    area = cv2.contourArea(contour)

    # 过滤小噪声
    if area > 500:
        # 计算圆度（周长²/面积）
        perimeter = cv2.arcLength(contour, True)
        circularity = (perimeter ** 2) / (4 * np.pi * area)

        # 圆度接近1表示是圆形
        if 0.7 < circularity < 1.3:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            count += 1

print(f"检测到 {count} 个硬币")
```

### 参数调优建议

**Canny阈值：**
- 先用自动阈值检测
- 根据效果微调：`edges = cv2.Canny(blur, lower, upper)`
- lower更小 → 检测更多边缘（可能含噪声）
- upper更大 → 只检测强边缘

**霍夫圆变换参数：**
- `param2`: 检测阈值
  - 太大 → 漏检
  - 太小 → 误检
  - 建议范围：20-50

- `minDist`: 圆心最小距离
  - 防止重复检测
  - 建议设为预期圆直径的0.5-1倍

### 交互式调试
```python
def nothing(x):
    pass

cv2.namedWindow('Canny')
cv2.createTrackbar('Threshold1', 'Canny', 50, 255, nothing)
cv2.createTrackbar('Threshold2', 'Canny', 150, 255, nothing)

while True:
    t1 = cv2.getTrackbarPos('Threshold1', 'Canny')
    t2 = cv2.getTrackbarPos('Threshold2', 'Canny')

    edges = cv2.Canny(blur, t1, t2)
    cv2.imshow('Canny', edges)

    if cv2.waitKey(1) == 27:
        break
```

## 扩展挑战（可选）

1. 同时检测圆形和矩形，分别计数
2. 根据硬币大小分类（大、中、小）
3. 实现实时视频中的硬币检测
4. 测试不同光照条件下的检测效果

## 常见问题

**Q: 为什么霍夫圆变换检测不到？**
A:
1. 检查边缘检测结果是否清晰
2. 降低param2参数（如改为20）
3. 调整minRadius和maxRadius范围

**Q: 为什么检测到重复的圆？**
A: 增大minDist参数

**Q: 如何验证检测结果是否正确？**
A:
1. 在原图上绘制检测到的圆
2. 目测检查圆的位置和大小
3. 统计数量并人工核对

**Q: 边缘检测效果差怎么办？**
A:
1. 先进行高斯滤波降噪
2. 尝试自适应阈值
3. 调整Canny参数或使用Otsu
