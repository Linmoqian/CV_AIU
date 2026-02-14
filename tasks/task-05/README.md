# Task 5: 实时颜色追踪

## 任务描述

从摄像头实时读取视频，追踪特定颜色的物体，并绘制轨迹。

## 任务要求

### 1. 摄像头读取（20分）
- 打开默认摄像头
- 读取视频帧
- 显示实时视频流

### 2. 颜色检测（40分）
- 定义追踪颜色的HSV范围（建议：红色或蓝色）
- 创建颜色掩膜
- 形态学去噪
- 查找颜色区域

### 3. 目标追踪（30分）
- 计算检测到的物体中心
- 绘制边界框和中心点
- 实时显示坐标信息
- 绘制运动轨迹

### 4. 可选功能（10分）
- 支持切换追踪颜色（按键切换）
- 显示追踪历史轨迹
- 保存追踪视频

## 提交要求

1. **代码文件**: `task5_solution.py`
2. **演示视频或截图**: 展示实时追踪效果
3. **保存的追踪结果**（如实现）:
   - `color_tracking_output.mp4`
   - 或 `tracking_trajectory.jpg`

## 评分标准

| 要求 | 分值 | 评分细则 |
|-----|------|---------|
| 摄像头读取 | 20分 | 成功打开并显示10分，流畅读取10分 |
| 颜色检测 | 40分 | HSV范围正确20分，检测准确20分 |
| 目标追踪 | 30分 | 边界框绘制15分，轨迹绘制15分 |
| 可选功能 | 10分 | 颜色切换或轨迹保存 |

## 提示

### 打开摄像头
```python
cap = cv2.VideoCapture(0)  # 0是默认摄像头

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # 处理frame...

    cv2.imshow('Color Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 颜色检测
```python
# 定义HSV范围
# 红色
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])

# 或蓝色
lower_blue = np.array([85, 100, 100])
upper_blue = np.array([135, 255, 255])

# 转HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# 创建掩膜
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)

# 形态学去噪
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
```

### 查找并追踪目标
```python
# 查找轮廓
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    area = cv2.contourArea(contour)

    if area > 500:  # 过滤小噪声
        # 获取边界框
        x, y, w, h = cv2.boundingRect(contour)

        # 计算中心点
        center_x = x + w // 2
        center_y = y + h // 2

        # 绘制边界框
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 绘制中心点
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

        # 显示坐标
        label = f'({center_x}, {center_y})'
        cv2.putText(frame, label, (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
```

### 绘制轨迹
```python
# 存储轨迹点
trajectory = []

max_length = 50  # 保留最近50个点

while True:
    ret, frame = cap.read()
    # ...

    # 检测到目标后
    if detected:
        trajectory.append((center_x, center_y))

        # 限制轨迹长度
        if len(trajectory) > max_length:
            trajectory.pop(0)

    # 绘制轨迹
    if len(trajectory) > 1:
        points = np.array(trajectory, dtype=np.int32)
        cv2.polylines(frame, [points], False, (255, 0, 0), 2)
```

### 切换颜色
```python
# 支持按键切换颜色
color_mode = 0  # 0: 红色, 1: 蓝色, 2: 绿色

while True:
    # ...

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('c'):  # 切换颜色
        color_mode = (color_mode + 1) % 3
        print(f"切换到颜色: {['红色', '蓝色', '绿色'][color_mode]}")

    # 根据color_mode选择颜色范围
    if color_mode == 0:
        # 红色
        ...
    elif color_mode == 1:
        # 蓝色
        ...
    else:
        # 绿色
        ...
```

### 保存视频
```python
# 创建VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 30
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    # 处理...

    # 写入帧
    out.write(frame)

    # ...

out.release()
```

## 完整代码框架

```python
import cv2
import numpy as np

# 全局变量
trajectory = []
color_mode = 0

def get_color_range(mode):
    """返回当前颜色的HSV范围"""
    colors = {
        0: {  # 红色
            'lower1': [0, 100, 100],
            'upper1': [10, 255, 255],
            'lower2': [170, 100, 100],
            'upper2': [180, 255, 255],
            'label': 'Red',
            'color': (0, 0, 255)
        },
        1: {  # 蓝色
            'lower': [85, 100, 100],
            'upper': [135, 255, 255],
            'label': 'Blue',
            'color': (255, 0, 0)
        },
        2: {  # 绿色
            'lower': [35, 100, 100],
            'upper': [85, 255, 255],
            'label': 'Green',
            'color': (0, 255, 0)
        }
    }
    return colors[mode]

def main():
    global trajectory, color_mode

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 转HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 获取当前颜色范围
        color_info = get_color_range(color_mode)

        # 创建掩膜
        if color_mode == 0:  # 红色特殊处理
            mask1 = cv2.inRange(hsv,
                              np.array(color_info['lower1']),
                              np.array(color_info['upper1']))
            mask2 = cv2.inRange(hsv,
                              np.array(color_info['lower2']),
                              np.array(color_info['upper2']))
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(hsv,
                              np.array(color_info['lower']),
                              np.array(color_info['upper']))

        # 形态学去噪
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # 查找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        detected = False

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                center_x = x + w // 2
                center_y = y + h // 2

                # 绘制
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                           color_info['color'], 2)
                cv2.circle(frame, (center_x, center_y), 5,
                          color_info['color'], -1)

                # 添加轨迹点
                trajectory.append((center_x, center_y))
                if len(trajectory) > 50:
                    trajectory.pop(0)

                detected = True
                break  # 只追踪一个目标

        # 绘制轨迹
        if len(trajectory) > 1:
            points = np.array(trajectory, dtype=np.int32)
            cv2.polylines(frame, [points], False, (0, 255, 255), 2)

        # 显示信息
        cv2.putText(frame, f"Color: {color_info['label']}",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                   0.7, color_info['color'], 2)

        if detected:
            cv2.putText(frame, f"Tracking: ON",
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                       0.7, (0, 255, 0), 2)

        cv2.imshow('Color Tracking', frame)

        # 键盘控制
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            color_mode = (color_mode + 1) % 3
            trajectory.clear()  # 清空轨迹

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
```

## 调试技巧

1. **显示掩膜窗口**：查看颜色提取是否准确
```python
cv2.imshow('Mask', mask)
```

2. **调整HSV范围**：先用静态图测试
```python
# 截图保存
cv2.imwrite('test_frame.jpg', frame)
# 离线调整参数
```

3. **打印调试信息**
```python
print(f"检测到 {len(contours)} 个轮廓")
print(f"目标中心: ({center_x}, {center_y})")
```

## 扩展挑战（可选）

1. 同时追踪多个颜色的物体
2. 追踪速度（计算帧间移动距离）
3. Kalman滤波预测目标位置
4. 多目标追踪（同时追踪多个同色物体）

## 常见问题

**Q: 摄像头打不开？**
A:
1. 检查摄像头是否被其他程序占用
2. 尝试不同的索引：`cv2.VideoCapture(1)`
3. 确认摄像头驱动正常

**Q: 颜色检测不准确？**
A:
1. 调整HSV范围的S和V值（如改为[50, 200, 50]到[15, 255, 255]）
2. 改善光照条件
3. 使用交互式工具获取准确的HSV值

**Q: 追踪不稳定？**
A:
1. 增大形态学操作的核
2. 调整面积阈值
3. 使用卡尔曼滤波平滑轨迹

**Q: 如何获取准确的HSV值？**
A:
```python
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        pixel = hsv[y, x]
        print(f"HSV: H={pixel[0]}, S={pixel[1]}, V={pixel[2]}")

cv2.setMouseCallback('Color Tracking', mouse_callback)
```
