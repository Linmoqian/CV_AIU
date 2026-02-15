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
显示辅助函数
提供方便的图像和视频显示功能
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def show_image(img, title='Image', size=(10, 8)):
    """
    显示单个图像

    参数:
        img: 图像（BGR格式）
        title: 窗口标题
        size: 显示大小（英寸）
    """
    # 转换为RGB（如果是BGR）
    if len(img.shape) == 3 and img.shape[2] == 3:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = img

    plt.figure(figsize=size)
    plt.imshow(img_rgb)
    plt.title(title)
    plt.axis('off')
    plt.show()


def show_images(images, titles=None, rows=1, size=(15, 5)):
    """
    显示多个图像

    参数:
        images: 图像列表
        titles: 标题列表
        rows: 行数
        size: 显示大小
    """
    n = len(images)
    cols = (n + rows - 1) // rows

    plt.figure(figsize=size)

    for i, img in enumerate(images):
        plt.subplot(rows, cols, i + 1)

        # 转换为RGB
        if len(img.shape) == 3 and img.shape[2] == 3:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = img

        plt.imshow(img_rgb, cmap='gray' if len(img.shape) == 2 else None)

        if titles and i < len(titles):
            plt.title(titles[i])

        plt.axis('off')

    plt.tight_layout()
    plt.show()


def show_images_cv(images, titles=None, wait_key=0):
    """
    使用OpenCV显示多个图像

    参数:
        images: 图像列表
        titles: 标题列表
        wait_key: 等待按键（0表示无限等待）
    """
    for i, img in enumerate(images):
        title = titles[i] if titles and i < len(titles) else f'Image {i}'
        cv2.imshow(title, img)

    cv2.waitKey(wait_key)
    cv2.destroyAllWindows()


def create_comparison(original, processed, title1='Original', title2='Processed'):
    """
    创建对比图

    参数:
        original: 原始图像
        processed: 处理后图像
        title1: 原图标题
        title2: 处理图标题

    返回:
        对比图
    """
    # 确保尺寸相同
    if original.shape != processed.shape:
        processed = cv2.resize(processed,
                              (original.shape[1], original.shape[0]))

    # 水平拼接
    comparison = np.hstack([original, processed])

    # 添加标题
    h, w = comparison.shape[:2]

    # 创建标题区域
    title_bar = np.zeros((60, w, 3), dtype=np.uint8)
    title_bar[:] = (255, 255, 255)

    # 添加文字
    cv2.putText(title_bar, title1, (20, 40),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(title_bar, title2, (w // 2 + 20, 40),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # 垂直拼接
    result = np.vstack([title_bar, comparison])

    return result


def show_comparison(original, processed, title1='Original', title2='Processed',
                   method='cv', size=(12, 6)):
    """
    显示对比图

    参数:
        original: 原始图像
        processed: 处理后图像
        title1: 原图标题
        title2: 处理图标题
        method: 显示方法 ('cv' 或 'matplotlib')
        size: 显示大小
    """
    comparison = create_comparison(original, processed, title1, title2)

    if method == 'cv':
        # 调整显示大小
        h, w = comparison.shape[:2]
        scale = min(size[0] / w, size[1] / h) * 0.8
        display = cv2.resize(comparison, None, fx=scale, fy=scale)
        cv2.imshow('Comparison', display)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        # 使用matplotlib
        comparison_rgb = cv2.cvtColor(comparison, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=size)
        plt.imshow(comparison_rgb)
        plt.axis('off')
        plt.show()


def create_grid(images, rows=None, cols=None, gap=10):
    """
    创建图像网格

    参数:
        images: 图像列表
        rows: 行数（None则自动计算）
        cols: 列数（None则自动计算）
        gap: 图像间隔（像素）

    返回:
        网格图像
    """
    n = len(images)

    if rows is None and cols is None:
        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))
    elif rows is None:
        rows = int(np.ceil(n / cols))
    elif cols is None:
        cols = int(np.ceil(n / rows))

    # 统一图像尺寸
    max_h = max(img.shape[0] for img in images)
    max_w = max(img.shape[1] for img in images)

    resized_images = []
    for img in images:
        if img.shape[:2] != (max_h, max_w):
            img = cv2.resize(img, (max_w, max_h))
        resized_images.append(img)

    # 计算网格大小
    grid_h = rows * max_h + (rows - 1) * gap
    grid_w = cols * max_w + (cols - 1) * gap

    # 创建空白画布
    if len(resized_images[0].shape) == 2:
        grid = np.zeros((grid_h, grid_w), dtype=np.uint8)
    else:
        grid = np.zeros((grid_h, grid_w, 3), dtype=np.uint8)

    # 填充网格
    for i, img in enumerate(resized_images):
        row = i // cols
        col = i % cols

        y = row * (max_h + gap)
        x = col * (max_w + gap)

        grid[y:y+max_h, x:x+max_w] = img

    return grid


def show_grid(images, rows=None, cols=None, gap=10, size=(12, 8)):
    """
    显示图像网格

    参数:
        images: 图像列表
        rows: 行数
        cols: 列数
        gap: 间隔
        size: 显示大小
    """
    grid = create_grid(images, rows, cols, gap)

    # 转换颜色空间
    if len(grid.shape) == 3:
        grid_rgb = cv2.cvtColor(grid, cv2.COLOR_BGR2RGB)
    else:
        grid_rgb = grid

    plt.figure(figsize=size)
    plt.imshow(grid_rgb, cmap='gray' if len(grid.shape) == 2 else None)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def add_info(img, text, position=(10, 30), color=(0, 255, 0),
             scale=0.7, thickness=2):
    """
    在图像上添加文字信息

    参数:
        img: 输入图像
        text: 文字内容
        position: 位置 (x, y)
        color: 颜色 (B, G, R)
        scale: 大小
        thickness: 粗细

    返回:
        添加文字后的图像
    """
    result = img.copy()

    # 添加背景
    (text_w, text_h), baseline = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)

    x, y = position
    cv2.rectangle(result,
                 (x - 5, y - text_h - 5),
                 (x + text_w + 5, y + baseline + 5),
                 (0, 0, 0), -1)

    # 添加文字
    cv2.putText(result, text, position,
               cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)

    return result


def show_histogram(img):
    """
    显示直方图

    参数:
        img: 输入图像
    """
    if len(img.shape) == 2:
        # 灰度图
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])

        plt.figure(figsize=(10, 4))
        plt.plot(hist, color='black')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.title('Grayscale Histogram')
        plt.grid(True)
        plt.show()

    else:
        # 彩色图
        colors = ['b', 'g', 'r']
        plt.figure(figsize=(10, 4))

        for i, color in enumerate(colors):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist, color=color, label=color.upper())

        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.title('Color Histogram')
        plt.legend()
        plt.grid(True)
        plt.show()


def interactive_threshold(img):
    """
    交互式阈值调整

    参数:
        img: 输入灰度图
    """
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def nothing(x):
        pass

    cv2.namedWindow('Threshold')

    cv2.createTrackbar('Threshold', 'Threshold', 127, 255, nothing)
    cv2.createTrackbar('Type', 'Threshold', 0, 4, nothing)

    types = ['BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']

    while True:
        thresh_val = cv2.getTrackbarPos('Threshold', 'Threshold')
        type_val = cv2.getTrackbarPos('Type', 'Threshold')

        # 阈值类型
        thresh_types = [
            cv2.THRESH_BINARY,
            cv2.THRESH_BINARY_INV,
            cv2.THRESH_TRUNC,
            cv2.THRESH_TOZERO,
            cv2.THRESH_TOZERO_INV
        ]

        ret, thresh = cv2.threshold(img, thresh_val, 255,
                                   thresh_types[type_val])

        # 显示对比
        comparison = np.hstack([img, thresh])
        display = cv2.resize(comparison, None, fx=0.8, fy=0.8)

        cv2.imshow('Threshold', display)

        if cv2.waitKey(1) == 27:  # ESC
            break

    cv2.destroyAllWindows()


# ==================== 使用示例 ====================
if __name__ == '__main__':
    import sys

    # 读取测试图像
    img_path = '../assets/sample-images/basic/landscape.jpg'

    if len(sys.argv) > 1:
        img_path = sys.argv[1]

    img = cv2.imread(img_path)

    if img is None:
        print(f"无法读取图像: {img_path}")
        exit()

    # 示例1：显示单个图像
    print("1. 显示单个图像")
    show_image(img, 'Test Image')

    # 示例2：显示多个图像
    print("2. 显示多个图像")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)

    show_images([img, gray, blur],
               ['Original', 'Grayscale', 'Blurred'],
               rows=1)

    # 示例3：显示对比图
    print("3. 显示对比图")
    show_comparison(img, blur, 'Original', 'Blurred', method='matplotlib')

    # 示例4：显示网格
    print("4. 显示网格")
    edges = cv2.Canny(gray, 50, 150)
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    show_grid([img, gray, blur, edges_bgr], rows=2, cols=2)

    # 示例5：添加信息
    print("5. 添加信息")
    result = add_info(img, 'OpenCV Display', (10, 30), (0, 255, 0))
    show_image(result, 'With Info')

    # 示例6：显示直方图
    print("6. 显示直方图")
    show_histogram(img)

    print("\n所有示例完成！")
