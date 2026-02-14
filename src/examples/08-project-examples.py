#                    _ooOoo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                   O\  =  /O
#                ____/`---'\____
#              .'  \|     |//  `.
#             /  \|||  :  |||//             /  _||||| -:- |||||-             |   | \\  -  /// |   |
#            | \_|  ''\---/''  |   |
#            \  .-\__  `-`  ___/-. /
#          ___`. .'  /--.--\  `. . __
#       ."" '<  `.___\_<|>_/___.'  >'"".
#      | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#      \  \ `-.   \_ __\ /__ _/   .-` /  /
# ======`-.____`-.___\_____/___.-`____.-'======
#                    `=---='
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#             佛祖保佑       永无BUG

"""
OpenCV示例：综合项目示例

学习目标:
    1. 文档扫描器实现
    2. 颜色识别分类器实现
    3. 简单人脸检测实现
"""

import cv2
import numpy as np
import sys
import os

# 添加utils目录到路径（兼容中文路径和Jupyter）
if "__file__" in globals():
    utils_path = os.path.join(os.path.dirname(__file__), "..", "utils")
else:
    utils_path = os.path.abspath(os.path.join("..", "utils"))
if os.path.exists(utils_path):
    sys.path.append(utils_path)
    from io_helpers import imread_chinese, get_image_path

print("综合项目示例")

# ==================== 项目1：文档扫描器 ====================
print("\n[项目1] 文档扫描器")

def document_scanner(img_path=None):
    """文档扫描器"""
    # 读取或创建测试图像
    if img_path:
        img = imread_chinese(img_path)
    else:
        print("  创建测试文档图像...")
        img = np.zeros((400, 600, 3), dtype=np.uint8)
        img[:] = (220, 220, 220)
        # 绘制文档内容
        for i in range(8):
            y = 60 + i * 40
            cv2.rectangle(img, (80, y), (520, y + 25), (0, 0, 0), -1)
        cv2.rectangle(img, (80, 20), (520, 50), (0, 0, 150), -1)

        # 添加透视畸变
        pts1 = np.float32([[0, 0], [600, 0], [600, 400], [0, 400]])
        pts2 = np.float32([[50, 30], [550, 50], [580, 380], [20, 350]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        img = cv2.warpPerspective(img, M, (600, 400))

    if img is None:
        print("  错误：无法读取图像")
        return None

    print("  [步骤1] 预处理...")
    # 转灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 高斯滤波
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Canny边缘检测
    edges = cv2.Canny(blur, 50, 150)

    print("  [步骤2] 查找文档轮廓...")
    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("  警告：未检测到轮廓")
        return None

    # 找最大轮廓
    doc_contour = max(contours, key=cv2.contourArea)

    # 多边形近似
    epsilon = 0.02 * cv2.arcLength(doc_contour, True)
    approx = cv2.approxPolyDP(doc_contour, epsilon, True)

    if len(approx) != 4:
        print(f"  警告：检测到{len(approx)}个点，需要4个")
        return None

    print("  [步骤3] 透视变换...")
    # 排序点：左上、右上、右下、左下
    pts = approx.reshape(4, 2)
    pts_sorted = np.zeros((4, 2), dtype=np.float32)

    # 按x坐标排序
    ind = np.lexsort((pts[:, 1], pts[:, 0]))
    pts = pts[ind]

    # 左边两个点
    left_points = pts[:2]
    right_points = pts[2:]

    # 左边按y排序
    left_points = left_points[np.argsort(left_points[:, 1])]
    right_points = right_points[np.argsort(right_points[:, 1])]

    pts_sorted[0] = left_points[0]  # 左上
    pts_sorted[3] = left_points[1]  # 左下
    pts_sorted[1] = right_points[0]  # 右上
    pts_sorted[2] = right_points[1]  # 右下

    # 计算新图像尺寸
    width_a = np.sqrt(((pts_sorted[2][0] - pts_sorted[3][0]) ** 2) +
                      ((pts_sorted[2][1] - pts_sorted[3][1]) ** 2))
    width_b = np.sqrt(((pts_sorted[1][0] - pts_sorted[0][0]) ** 2) +
                      ((pts_sorted[1][1] - pts_sorted[0][1]) ** 2))
    max_width = max(int(width_a), int(width_b))

    height_a = np.sqrt(((pts_sorted[1][0] - pts_sorted[2][0]) ** 2) +
                       ((pts_sorted[1][1] - pts_sorted[2][1]) ** 2))
    height_b = np.sqrt(((pts_sorted[0][0] - pts_sorted[3][0]) ** 2) +
                       ((pts_sorted[0][1] - pts_sorted[3][1]) ** 2))
    max_height = max(int(height_a), int(height_b))

    # 目标点
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype=np.float32)

    # 透视变换
    M = cv2.getPerspectiveTransform(pts_sorted, dst)
    warped = cv2.warpPerspective(img, M, (max_width, max_height))

    print("  [步骤4] 图像增强...")
    # 转灰度
    warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    # 自适应阈值
    scanned = cv2.adaptiveThreshold(warped_gray, 255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)

    print("  [完成] 文档扫描完成！")

    return img, warped, scanned

# 运行文档扫描器
result = document_scanner()
if result:
    original, warped, scanned = result

    # 显示结果（调整尺寸以匹配）
    height, width = original.shape[:2]
    warped_resized = cv2.resize(warped, (width, height))
    scanned_resized = cv2.resize(cv2.cvtColor(scanned, cv2.COLOR_GRAY2BGR),
                                  (width, height))

    row1 = np.hstack([original, warped_resized])
    row2 = np.hstack([scanned_resized, np.zeros_like(original)])
    result_all = np.vstack([row1, row2])
    result_all = cv2.resize(result_all, None, fx=0.5, fy=0.5)

    cv2.imshow('Document Scanner', result_all)
    print("\n按任意键继续...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存功能已禁用
    # cv2.imwrite('scanner_original.jpg', original)
    # cv2.imwrite('scanner_warped.jpg', warped)
    # cv2.imwrite('scanner_scanned.jpg', scanned)
    print("  [提示] 图片保存功能已禁用")

# ==================== 项目2：颜色识别分类器 ====================
print("\n[项目2] 颜色识别分类器")

def color_classifier(img_path=None):
    """颜色识别分类器"""
    # 读取或创建测试图像
    if img_path:
        img = imread_chinese(img_path)
    else:
        print("  创建测试图像...")
        img = np.zeros((400, 600, 3), dtype=np.uint8)
        img[:] = (240, 240, 240)
        # 绘制不同颜色的圆形
        cv2.circle(img, (100, 200), 60, (0, 0, 255), -1)  # 红
        cv2.circle(img, (250, 200), 60, (0, 255, 0), -1)  # 绿
        cv2.circle(img, (400, 200), 60, (255, 0, 0), -1)  # 蓝
        cv2.circle(img, (525, 200), 60, (0, 255, 255), -1)  # 黄

    if img is None:
        print("  错误：无法读取图像")
        return None

    # 定义颜色范围
    COLORS = {
        'red': {
            'lower': [0, 100, 100],
            'upper': [10, 255, 255],
            'label': 'Red',
            'color': (0, 0, 255)
        },
        'green': {
            'lower': [35, 100, 100],
            'upper': [85, 255, 255],
            'label': 'Green',
            'color': (0, 255, 0)
        },
        'blue': {
            'lower': [85, 100, 100],
            'upper': [135, 255, 255],
            'label': 'Blue',
            'color': (255, 0, 0)
        },
        'yellow': {
            'lower': [20, 100, 100],
            'upper': [35, 255, 255],
            'label': 'Yellow',
            'color': (0, 255, 255)
        }
    }

    print("  检测颜色...")

    result_img = img.copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 检测每种颜色
    for color_name, color_info in COLORS.items():
        lower = np.array(color_info['lower'])
        upper = np.array(color_info['upper'])

        # 创建掩膜
        mask = cv2.inRange(hsv, lower, upper)

        # 形态学去噪
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # 查找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        count = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # 过滤小噪声
                # 获取边界框
                x, y, w, h = cv2.boundingRect(contour)

                # 绘制边界框
                cv2.rectangle(result_img, (x, y), (x + w, y + h),
                           color_info['color'], 2)

                # 添加标签
                label = f"{color_info['label']}"
                cv2.putText(result_img, label, (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                           color_info['color'], 2)

                count += 1

        print(f"    {color_name.capitalize()}: {count} 个")

    print("  [完成] 颜色检测完成！")

    return img, result_img

# 运行颜色分类器
result = color_classifier()
if result:
    original, result_img = result

    # 显示结果
    row = np.hstack([original, result_img])
    row = cv2.resize(row, None, fx=0.6, fy=0.6)

    cv2.imshow('Color Classification', row)
    print("\n按任意键继续...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存功能已禁用
    # cv2.imwrite('color_detection_result.jpg', result_img)
    print("  [提示] 图片保存功能已禁用")

# ==================== 项目3：简单人脸检测 ====================
print("\n[项目3] 简单人脸检测")

def face_detector(img_path=None):
    """人脸检测"""
    # 加载Haar级联分类器
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml'
    )

    # 读取或创建测试图像
    if img_path:
        img = imread_chinese(img_path)
    else:
        print("  使用assets中的face.jpg...")
        img = imread_chinese('../assets/sample-images/real-world/face.jpg')
        if img is None:
            print("  face.jpg不存在，创建测试人脸图像...")
            img = np.zeros((400, 400, 3), dtype=np.uint8)
            img[:] = (200, 200, 200)
            # 脸部轮廓
            cv2.ellipse(img, (200, 200), (150, 200), 0, 0, 360, (180, 160, 140), -1)
            # 眼睛
            cv2.ellipse(img, (130, 160), (30, 20), 0, 0, 360, (255, 255, 255), -1)
            cv2.ellipse(img, (270, 160), (30, 20), 0, 0, 360, (255, 255, 255), -1)
            cv2.circle(img, (130, 160), 10, (0, 0, 0), -1)
            cv2.circle(img, (270, 160), 10, (0, 0, 0), -1)
            # 眉毛
            cv2.line(img, (100, 130), (160, 130), (50, 30, 10), 5)
            cv2.line(img, (240, 130), (300, 130), (50, 30, 10), 5)
            # 鼻子
            pts = np.array([[200, 180], [180, 240], [220, 240]], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.fillPoly(img, [pts], (150, 130, 110))
            # 嘴巴
            cv2.ellipse(img, (200, 290), (50, 25), 0, 0, 180, (100, 50, 50), 3)

    if img is None:
        print("  错误：无法读取图像")
        return None

    print("  检测人脸...")

    # 转灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 检测人脸
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print(f"    检测到 {len(faces)} 个人脸")

    result_img = img.copy()

    for (x, y, w, h) in faces:
        # 绘制人脸矩形框
        cv2.rectangle(result_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # 检测眼睛
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = result_img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh),
                         (0, 255, 0), 2)

    print("  [完成] 人脸检测完成！")

    return img, result_img

# 运行人脸检测
result = face_detector()
if result:
    original, result_img = result

    # 显示结果
    row = np.hstack([original, result_img])
    row = cv2.resize(row, None, fx=0.6, fy=0.6)

    cv2.imshow('Face Detection', row)
    print("\n按任意键退出...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存功能已禁用
    # cv2.imwrite('face_detection_result.jpg', result_img)
    print("  [提示] 图片保存功能已禁用")

print("所有项目演示完成！")
