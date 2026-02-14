"""
图像处理模板
用于快速开始图像处理任务
"""

import cv2
import numpy as np
import os

class ImageProcessor:
    """图像处理类"""

    def __init__(self, img_path=None):
        """
        初始化

        参数:
            img_path: 图像路径（可选）
        """
        self.img = None
        self.gray = None
        self.hsv = None

        if img_path:
            self.load_image(img_path)

    def load_image(self, img_path):
        """
        加载图像

        参数:
            img_path: 图像路径

        返回:
            bool: 是否成功
        """
        self.img = cv2.imread(img_path)

        if self.img is None:
            print(f"错误: 无法读取图像 {img_path}")
            return False

        print(f"成功读取图像: {self.img.shape}")
        return True

    def preprocess(self):
        """预处理：转灰度和HSV"""
        if self.img is None:
            print("错误: 请先加载图像")
            return False

        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        print("预处理完成")
        return True

    def resize(self, width=None, height=None, scale=None):
        """
        调整图像大小

        参数:
            width: 目标宽度
            height: 目标高度
            scale: 缩放因子

        返回:
            调整后的图像
        """
        if self.img is None:
            print("错误: 请先加载图像")
            return None

        if scale:
            return cv2.resize(self.img, None, fx=scale, fy=scale)

        if width and height:
            return cv2.resize(self.img, (width, height))

        if width:
            scale = width / self.img.shape[1]
            new_height = int(self.img.shape[0] * scale)
            return cv2.resize(self.img, (width, new_height))

        if height:
            scale = height / self.img.shape[0]
            new_width = int(self.img.shape[1] * scale)
            return cv2.resize(self.img, (new_width, height))

        return self.img

    def crop(self, x1, y1, x2, y2):
        """
        裁剪图像

        参数:
            x1, y1: 左上角坐标
            x2, y2: 右下角坐标

        返回:
            裁剪后的图像
        """
        if self.img is None:
            print("错误: 请先加载图像")
            return None

        return self.img[y1:y2, x1:x2].copy()

    def filter_blur(self, method='gaussian', kernel_size=5):
        """
        图像滤波

        参数:
            method: 滤波方法 ('mean', 'gaussian', 'median', 'bilateral')
            kernel_size: 核大小

        返回:
            滤波后的图像
        """
        if self.img is None:
            print("错误: 请先加载图像")
            return None

        if method == 'mean':
            return cv2.blur(self.img, (kernel_size, kernel_size))

        elif method == 'gaussian':
            return cv2.GaussianBlur(self.img, (kernel_size, kernel_size), 0)

        elif method == 'median':
            return cv2.medianBlur(self.img, kernel_size)

        elif method == 'bilateral':
            return cv2.bilateralFilter(self.img, 15, 80, 80)

        else:
            print(f"错误: 未知的滤波方法 {method}")
            return None

    def detect_edges(self, method='canny', threshold1=50, threshold2=150):
        """
        边缘检测

        参数:
            method: 检测方法 ('canny', 'sobel')
            threshold1: 低阈值
            threshold2: 高阈值

        返回:
            边缘图像
        """
        if self.gray is None:
            print("错误: 请先调用preprocess()")
            return None

        if method == 'canny':
            return cv2.Canny(self.gray, threshold1, threshold2)

        elif method == 'sobel':
            sobelx = cv2.Sobel(self.gray, cv2.CV_64F, 1, 0, ksize=3)
            sobelx = np.uint8(np.absolute(sobelx))
            return sobelx

        else:
            print(f"错误: 未知的边缘检测方法 {method}")
            return None

    def threshold(self, method='adaptive', value=127):
        """
        图像阈值

        参数:
            method: 阈值方法 ('simple', 'otsu', 'adaptive')
            value: 阈值

        返回:
            二值图像
        """
        if self.gray is None:
            print("错误: 请先调用preprocess()")
            return None

        if method == 'simple':
            ret, thresh = cv2.threshold(self.gray, value, 255, cv2.THRESH_BINARY)
            return thresh

        elif method == 'otsu':
            ret, thresh = cv2.threshold(self.gray, 0, 255,
                                       cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            print(f"Otsu阈值: {ret}")
            return thresh

        elif method == 'adaptive':
            return cv2.adaptiveThreshold(self.gray, 255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)

        else:
            print(f"错误: 未知的阈值方法 {method}")
            return None

    def extract_color(self, color_name='red'):
        """
        颜色提取

        参数:
            color_name: 颜色名称 ('red', 'green', 'blue', 'yellow')

        返回:
            掩膜和结果图像
        """
        if self.hsv is None:
            print("错误: 请先调用preprocess()")
            return None, None

        # 定义颜色范围
        colors = {
            'red': {
                'lower1': [0, 100, 100],
                'upper1': [10, 255, 255],
                'lower2': [170, 100, 100],
                'upper2': [180, 255, 255]
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

        if color_name not in colors:
            print(f"错误: 未知的颜色 {color_name}")
            return None, None

        color_info = colors[color_name]

        # 创建掩膜
        if color_name == 'red':
            mask1 = cv2.inRange(self.hsv,
                              np.array(color_info['lower1']),
                              np.array(color_info['upper1']))
            mask2 = cv2.inRange(self.hsv,
                              np.array(color_info['lower2']),
                              np.array(color_info['upper2']))
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(self.hsv,
                              np.array(color_info['lower']),
                              np.array(color_info['upper']))

        # 形态学去噪
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # 应用掩膜
        result = cv2.bitwise_and(self.img, self.img, mask=mask)

        return mask, result

    def morphology(self, operation='open', kernel_size=5):
        """
        形态学操作

        参数:
            operation: 操作类型 ('erode', 'dilate', 'open', 'close', 'gradient')
            kernel_size: 核大小

        返回:
            处理后的图像
        """
        if self.gray is None:
            print("错误: 请先调用preprocess()")
            return None

        # 先转二值
        ret, binary = cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY)

        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        if operation == 'erode':
            return cv2.erode(binary, kernel, iterations=1)

        elif operation == 'dilate':
            return cv2.dilate(binary, kernel, iterations=1)

        elif operation == 'open':
            return cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        elif operation == 'close':
            return cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        elif operation == 'gradient':
            return cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

        else:
            print(f"错误: 未知的形态学操作 {operation}")
            return None

    def save(self, img, output_path):
        """
        保存图像

        参数:
            img: 要保存的图像
            output_path: 输出路径
        """
        cv2.imwrite(output_path, img)
        print(f"图像已保存: {output_path}")

    def show(self, img, window_name='Image'):
        """
        显示图像

        参数:
            img: 要显示的图像
            window_name: 窗口名称
        """
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# ==================== 使用示例 ====================
if __name__ == '__main__':
    # 创建处理器
    processor = ImageProcessor()

    # 加载图像
    if not processor.load_image('../assets/sample-images/basic/landscape.jpg'):
        exit()

    # 预处理
    processor.preprocess()

    # 调整大小
    resized = processor.resize(width=400)
    processor.show(resized, 'Resized')

    # 滤波
    blurred = processor.filter_blur(method='gaussian', kernel_size=5)
    processor.show(blurred, 'Blurred')

    # 边缘检测
    edges = processor.detect_edges(method='canny', threshold1=50, threshold2=150)
    processor.show(edges, 'Edges')

    # 保存结果
    processor.save(edges, 'edges_output.jpg')

    print("\n模板使用完成！")
