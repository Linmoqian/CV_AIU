# Task 2: 色彩空间转换与颜色提取

## 任务描述

使用HSV色彩空间从图像中提取特定颜色的物体，并统计数量。

## 任务要求

### 1. 色彩空间转换（30分）
- 读取一张包含红色物体的图像
- 将图像从BGR转换为HSV色彩空间
- 分别显示H、S、V三个通道

### 2. 颜色提取（40分）
- 定义红色的HSV范围
- 创建掩膜提取红色区域
- 应用掩膜显示提取结果

### 3. 颜色识别函数（30分）
- 编写一个通用函数，可以提取任意颜色
- 函数参数：图像、颜色名称
- 支持的颜色：红、绿、蓝、黄

## 提交要求

1. **代码文件**: `task2_solution.py`
2. **运行截图**: 显示原图、掩膜和提取结果
3. **保存的图像**:
   - `hsv_channels.jpg`（H、S、V三通道并排）
   - `red_mask.jpg`
   - `red_extracted.jpg`

## 评分标准

| 要求 | 分值 | 评分细则 |
|-----|------|---------|
| HSV转换 | 15分 | 正确转换为HSV |
| 通道分离 | 15分 | 正确显示三个通道 |
| 红色提取 | 20分 | HSV范围正确10分，掩膜正确10分 |
| 结果显示 | 20分 | 掩膜清晰10分，提取结果准确10分 |
| 通用函数 | 30分 | 函数设计合理15分，支持多种颜色15分 |

## 参考代码

### HSV颜色范围

```python
import numpy as np

# 常见颜色的HSV范围
COLORS = {
    'red': {
        'lower': [0, 100, 100],
        'upper': [10, 255, 255]
    },
    'green': {
        'lower': [35, 100, 100],
        'upper': [85, 255, 255]
    },
    'blue': {
        'lower': [85, 100, 100],
        'upper': [135, 255, 255]
    },
    'yellow': {
        'lower': [20, 100, 100],
        'upper': [35, 255, 255]
    }
}
```

### 颜色提取函数模板

```python
def extract_color(img, color_name):
    """
    从图像中提取指定颜色

    参数:
        img: 输入图像（BGR格式）
        color_name: 颜色名称 ('red', 'green', 'blue', 'yellow')

    返回:
        mask: 二值掩膜
        result: 提取结果图像
    """
    # 1. 转HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 获取颜色范围
    # TODO: 完成代码

    # 3. 创建掩膜
    # TODO: 完成代码

    # 4. 应用掩膜
    # TODO: 完成代码

    return mask, result
```

## 测试图像建议

可以使用以下图像进行测试：
- 红苹果
- 蓝球
- 绿叶
- 黄色物体

## 提示

### 红色特殊处理

红色在HSV空间跨越0和180，需要两个范围：

```python
# 第一个范围：0-10
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])

# 第二个范围：170-180
lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])

# 创建两个掩膜并合并
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)
```

### 形态学去噪

```python
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
```

## 扩展挑战（可选）

1. 实现交互式颜色选择器（点击图像获取HSV值）
2. 支持自定义HSV范围
3. 同时提取并显示多种颜色
4. 统计每种颜色的像素数量

## 常见问题

**Q: 为什么提取的颜色不准确？**
A:
1. 调整HSV范围，适当放宽S和V的范围
2. 添加形态学操作去除噪声
3. 检查光照条件，光照不均会影响效果

**Q: 如何获取图像中某个颜色的HSV值？**
A: 使用以下代码：

```python
def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        pixel = hsv[y, x]
        print(f"HSV: H={pixel[0]}, S={pixel[1]}, V={pixel[2]}")

cv2.setMouseCallback('image', get_hsv_value)
```

**Q: 红色提取效果差？**
A: 红色需要两个范围，记得合并两个掩膜
