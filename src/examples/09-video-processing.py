"""
OpenCV示例：视频处理

学习目标:
    1. 读取和显示视频
    2. 从摄像头读取
    3. 保存视频
    4. 实时处理视频帧
"""

import cv2
import numpy as np

print("视频处理示例")

# ==================== 1. 读取视频文件 ====================
print("\n1. 读取视频文件")

# 尝试打开视频文件（如果不存在会提示）
video_path = '../assets/test-videos/color-tracking.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"  警告：无法打开视频文件 {video_path}")
    print("  提示：请将测试视频放在 assets/test-videos/ 目录下")
    print("  继续使用摄像头演示...")
    use_webcam = True
else:
    print(f"  [OK] 打开视频: {video_path}")
    use_webcam = False

# ==================== 2. 视频属性 ====================
if not use_webcam:
    # 获取视频属性
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"\n视频属性:")
    print(f"  帧率: {fps} FPS")
    print(f"  总帧数: {frame_count}")
    print(f"  分辨率: {width}x{height}")
    print(f"  时长: {frame_count/fps:.2f} 秒")

# ==================== 3. 处理视频帧 ====================
print("\n2. 实时处理视频")
print("  操作: 边缘检测 + 高斯模糊")
print("  提示: 按 'q' 退出, 按 'p' 暂停\n")

if use_webcam:
    cap = cv2.VideoCapture(0)  # 打开默认摄像头
    print("  [摄像头] 按 'q' 退出\n")

frame_count = 0
paused = False

while True:
    if not paused:
        ret, frame = cap.read()

        if not ret:
            if use_webcam:
                print("  无法读取摄像头")
            else:
                print("  视频结束")
            break

        frame_count += 1

        # 处理帧
        # 转灰度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 高斯模糊
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Canny边缘检测
        edges = cv2.Canny(blurred, 50, 150)

        # 转回BGR用于显示
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # 并排显示
        display = np.hstack([frame, edges_bgr])
        display = cv2.resize(display, None, fx=0.7, fy=0.7)

        # 添加帧数
        cv2.putText(display, f'Frame: {frame_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Video Processing', display)

    # 键盘控制
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):  # 退出
        break
    elif key == ord('p'):  # 暂停/继续
        paused = not paused
        print(f"  {'暂停' if paused else '继续'}")

cap.release()
cv2.destroyAllWindows()

print(f"\n  处理了 {frame_count} 帧")
print("  [完成] 视频处理结束\n")

# ==================== 4. 颜色追踪示例 ====================
print("3. 实时颜色追踪")
print("  追踪颜色: 红色")
print("  提示: 按 'q' 退出\n")

# 打开摄像头
cap = cv2.VideoCapture(0)

# 定义红色的HSV范围
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 100, 100])
upper_red2 = np.array([180, 255, 255])

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("  无法读取摄像头")
        break

    frame_count += 1

    # 转HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 创建红色掩膜
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # 形态学去噪
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # 绘制检测结果
    result = frame.copy()

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 500:  # 过滤小噪声
            # 获取边界框
            x, y, w, h = cv2.boundingRect(contour)

            # 绘制边界框
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 计算中心点
            center_x = x + w // 2
            center_y = y + h // 2

            # 绘制中心点
            cv2.circle(result, (center_x, center_y), 5, (0, 0, 255), -1)

            # 显示坐标
            label = f'({center_x}, {center_y})'
            cv2.putText(result, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # 显示面积
            area_label = f'Area: {area}'
            cv2.putText(result, area_label, (x, y + h + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 显示掩膜和结果
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    display = np.hstack([result, mask_bgr])
    display = cv2.resize(display, None, fx=0.7, fy=0.7)

    # 添加帧数
    cv2.putText(display, f'Frame: {frame_count}', (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Red Color Tracking', display)

    # 按q退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"\n  处理了 {frame_count} 帧")
print("  [完成] 颜色追踪结束\n")

# ==================== 5. 保存视频示例 ====================
print("4. 保存视频示例")
print("  提示：录制5秒视频并保存\n")

# 打开摄像头
cap = cv2.VideoCapture(0)

# 获取视频属性
fps = 30
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 定义编码器
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# 创建VideoWriter对象
output_path = 'output_video.mp4'
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

print(f"  开始录制...")
print(f"  输出: {output_path}")
print(f"  分辨率: {width}x{height}")
print(f"  帧率: {fps} FPS")
print("  倒计时: 5秒\n")

# 录制5秒
frames_to_record = 5 * fps  # 5秒 * 30fps
frame_count = 0

while frame_count < frames_to_record:
    ret, frame = cap.read()

    if not ret:
        break

    # 添加倒计时
    remaining = int((frames_to_record - frame_count) / fps)
    cv2.putText(frame, f'Recording... {remaining}s', (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 写入帧
    out.write(frame)

    # 显示
    cv2.imshow('Recording', frame)

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 显示进度
    if frame_count % 30 == 0:
        print(f"  进度: {frame_count/fps:.1f}秒 / 5.0秒")

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"\n  [完成] 视频已保存: {output_path}")
print(f"  总帧数: {frame_count}")

print("视频处理示例完成！")

print("\n提示:")
print("  - 如果没有摄像头，请将测试视频放在 assets/test-videos/ 目录")
print("  - 支持的格式: .mp4, .avi, .mov")
print("  - 可以使用手机录制视频进行测试")
