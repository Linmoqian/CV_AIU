                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \|     |//  `.
            /  \|||  :  |||//             /  _||||| -:- |||||-             |   | \\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            佛祖保佑       永无BUG

"""
图像辅助函数
提供常用的图像处理辅助功能
"""

import cv2
import numpy as np


def load_image_or_exit(img_path, gray=False, verbose=True):
    """
    加载图像，失败则退出

    参数:
        img_path: 图像路径
        gray: 是否转为灰度图
        verbose: 是否打印信息

    返回:
        图像或None
    """
    img = cv2.imread(img_path)

    if img is None:
        print(f"错误: 无法读取图像 {img_path}")
        print("请检查：")
        print("  1. 文件路径是否正确")
        print("  2. 文件是否存在")
        print("  3. 路径中不要包含中文")
        return None

    if gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if verbose:
        print(f"成功读取图像: {img_path}")
        print(f"  尺寸: {img.shape}")

    return img


def save_image(img, output_path, verbose=True):
    """
    保存图像

    参数:
        img: 图像
        output_path: 输出路径
        verbose: 是否打印信息

    返回:
        bool: 是否成功
    """
    try:
        cv2.imwrite(output_path, img)

        if verbose:
            print(f"图像已保存: {output_path}")

        return True

    except Exception as e:
        print(f"保存失败: {e}")
        return False


def resize_keep_aspect(img, target_width=None, target_height=None):
    """
    保持宽高比缩放

    参数:
        img: 输入图像
        target_width: 目标宽度
        target_height: 目标高度

    返回:
        缩放后的图像
    """
    h, w = img.shape[:2]

    if target_width:
        scale = target_width / w
        new_h = int(h * scale)
        return cv2.resize(img, (target_width, new_h))

    if target_height:
        scale = target_height / h
        new_w = int(w * scale)
        return cv2.resize(img, (new_w, target_height))

    return img


def crop_center(img, crop_width, crop_height):
    """
    裁剪图像中心区域

    参数:
        img: 输入图像
        crop_width: 裁剪宽度
        crop_height: 裁剪高度

    返回:
        裁剪后的图像
    """
    h, w = img.shape[:2]

    start_x = max(0, (w - crop_width) // 2)
    start_y = max(0, (h - crop_height) // 2)

    return img[start_y:start_y+crop_height, start_x:start_x+crop_width]


def add_watermark(img, text, position='bottom-right',
                  alpha=0.5, color=(255, 255, 255), scale=1.0):
    """
    添加水印

    参数:
        img: 输入图像
        text: 水印文字
        position: 位置 ('top-left', 'top-right', 'bottom-left', 'bottom-right')
        alpha: 透明度
        color: 颜色 (B, G, R)
        scale: 文字大小

    返回:
        添加水印后的图像
    """
    result = img.copy()
    h, w = result.shape[:2]

    # 获取文字大小
    (text_w, text_h), baseline = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)

    # 计算位置
    if position == 'top-left':
        x, y = 10, text_h + 10
    elif position == 'top-right':
        x, y = w - text_w - 10, text_h + 10
    elif position == 'bottom-left':
        x, y = 10, h - 10
    else:  # bottom-right
        x, y = w - text_w - 10, h - 10

    # 创建水印层
    overlay = result.copy()

    # 添加文字
    cv2.putText(overlay, text, (x, y),
               cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2)

    # 混合
    result = cv2.addWeighted(result, 1 - alpha, overlay, alpha, 0)

    return result


def auto_canny(img, sigma=0.33):
    """
    自动Canny边缘检测

    参数:
        img: 输入灰度图
        sigma: 调整系数

    返回:
        边缘图像
    """
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 计算中值
    v = np.median(img)

    # 应用Canny
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    edged = cv2.Canny(img, lower, upper)

    return edged


def sort_contours(cnts, method='left-to-right'):
    """
    排序轮廓

    参数:
        cnts: 轮廓列表
        method: 排序方法 ('left-to-right', 'right-to-left',
                          'top-to-bottom', 'bottom-to-top')

    返回:
        排序后的轮廓列表和边界框列表
    """
    bounding_boxes = [cv2.boundingRect(c) for c in cnts]

    if method == 'left-to-right' or method == 'top-to-bottom':
        cnts, bounding_boxes = zip(*sorted(zip(cnts, bounding_boxes),
                                           key=lambda b: b[1][0] if method == 'left-to-right' else b[1][1]))

    else:  # right-to-left or bottom-to-top
        cnts, bounding_boxes = zip(*sorted(zip(cnts, bounding_boxes),
                                           key=lambda b: -b[1][0] if method == 'right-to-left' else -b[1][1]))

    return cnts, bounding_boxes


def draw_contours_info(img, contours, color=(0, 255, 0), thickness=2):
    """
    绘制轮廓并添加信息

    参数:
        img: 输入图像
        contours: 轮廓列表
        color: 颜色
        thickness: 线宽

    返回:
        绘制后的图像
    """
    result = img.copy()

    for i, contour in enumerate(contours):
        # 获取边界框
        x, y, w, h = cv2.boundingRect(contour)

        # 计算面积
        area = cv2.contourArea(contour)

        # 绘制矩形
        cv2.rectangle(result, (x, y), (x + w, y + h), color, thickness)

        # 添加文字
        label = f'#{i+1}'
        label += f' A:{area:.0f}'

        cv2.putText(result, label, (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    return result


def get_dominant_color(img, k=1):
    """
    获取图像主要颜色（使用K-means）

    参数:
        img: 输入图像
        k: 颜色数量

    返回:
        主要颜色列表
    """
    # 转换为RGB并reshape
    data = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data = data.reshape((-1, 3))

    # 转float32
    data = np.float32(data)

    # 定义criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # K-means聚类
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10,
                                   cv2.KMEANS_RANDOM_CENTERS)

    # 转回uint8
    centers = np.uint8(centers)

    return centers.tolist()


def create_checkerboard(rows, cols, square_size):
    """
    创建棋盘格图像

    参数:
        rows: 行数
        cols: 列数
        square_size: 方块大小（像素）

    返回:
        棋盘格图像
    """
    board_size = square_size * max(rows, cols)
    img = np.zeros((board_size, board_size), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            if (i + j) % 2 == 0:
                y1, y2 = i * square_size, (i + 1) * square_size
                x1, x2 = j * square_size, (j + 1) * square_size
                img[y1:y2, x1:x2] = 255

    return img


def adjust_brightness_contrast(img, brightness=0, contrast=0):
    """
    调整亮度和对比度

    参数:
        img: 输入图像
        brightness: 亮度调整（-100到100）
        contrast: 对比度调整（-100到100）

    返回:
        调整后的图像
    """
    brightness = np.clip(brightness, -100, 100)
    contrast = np.clip(contrast, -100, 100)

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha = f
        beta = 127 * (1 - f)
    else:
        alpha = 1
        beta = 0

    if brightness != 0:
        beta += brightness

    result = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    return result


def skeletonize(img):
    """
    骨架化（细化）

    参数:
        img: 输入二值图

    返回:
        骨架图像
    """
    # 确保是二值图
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    # 二值化
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # 形态学细化
    skeleton = np.zeros(binary.shape, np.uint8)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    while True:
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        temp = cv2.subtract(binary, opened)
        eroded = cv2.erode(temp, kernel)

        skeleton = cv2.bitwise_or(skeleton, eroded)
        binary = cv2.erode(binary, kernel)

        if cv2.countNonZero(binary) == 0:
            break

    return skeleton


def remove_border(img, border_size=10):
    """
    移除图像边框

    参数:
        img: 输入图像
        border_size: 边框大小

    返回:
        移除边框后的图像
    """
    h, w = img.shape[:2]

    return img[border_size:h-border_size, border_size:w-border_size]


def add_border(img, border_size=10, color=(0, 0, 0), type_=cv2.BORDER_CONSTANT):
    """
    添加边框

    参数:
        img: 输入图像
        border_size: 边框大小
        color: 边框颜色
        type_: 边框类型

    返回:
        添加边框后的图像
    """
    return cv2.copyMakeBorder(img, border_size, border_size,
                            border_size, border_size,
                            type_, value=color)


# ==================== 使用示例 ====================
if __name__ == '__main__':
    import sys

    # 读取测试图像
    img_path = '../assets/sample-images/basic/landscape.jpg'

    if len(sys.argv) > 1:
        img_path = sys.argv[1]

    img = load_image_or_exit(img_path)

    if img is None:
        exit()

    # 示例1：保持宽高比缩放
    print("1. 保持宽高比缩放")
    resized = resize_keep_aspect(img, target_width=400)
    save_image(resized, 'resized.jpg')

    # 示例2：裁剪中心
    print("2. 裁剪中心区域")
    cropped = crop_center(img, 300, 300)
    save_image(cropped, 'cropped.jpg')

    # 示例3：添加水印
    print("3. 添加水印")
    watermarked = add_watermark(img, 'OpenCV Training',
                               position='bottom-right',
                               alpha=0.5, scale=1.5)
    save_image(watermarked, 'watermarked.jpg')

    # 示例4：自动Canny
    print("4. 自动Canny边缘检测")
    edges = auto_canny(img)
    save_image(edges, 'auto_edges.jpg')

    # 示例5：调整亮度和对比度
    print("5. 调整亮度和对比度")
    adjusted = adjust_brightness_contrast(img, brightness=30, contrast=30)
    save_image(adjusted, 'adjusted.jpg')

    # 示例6：创建棋盘格
    print("6. 创建棋盘格")
    checkerboard = create_checkerboard(8, 8, 50)
    save_image(checkerboard, 'checkerboard.jpg')

    print("\n所有示例完成！")
