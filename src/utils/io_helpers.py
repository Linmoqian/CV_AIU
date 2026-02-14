"""
OpenCV中文路径辅助工具

解决OpenCV的cv2.imread()和cv2.imwrite()不支持中文路径的问题
"""

import cv2
import numpy as np
import os


def imread_chinese(path, flags=-1):
    """
    读取包含中文路径的图片

    参数:
        path: 图片路径（支持中文）
        flags: 读取标志，默认为-1（保持原格式）
               cv2.IMREAD_COLOR (-1): 彩色图（默认）
               cv2.IMREAD_GRAYSCALE (0): 灰度图
               cv2.IMREAD_UNCHANGED (1): 包含alpha通道

    返回:
        img: 图片数组，如果读取失败返回None
    """
    if not os.path.exists(path):
        return None
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), flags)
    return img


def imwrite_chinese(path, img):
    """
    保存图片到包含中文的路径

    参数:
        path: 保存路径（支持中文）
        img: 要保存的图片数组

    返回:
        bool: 保存成功返回True，失败返回False
    """
    try:
        ext = os.path.splitext(path)[1]
        cv2.imencode(ext, img)[1].tofile(path)
        return True
    except Exception as e:
        print(f"保存失败: {e}")
        return False


def get_image_path(relative_path, attempts=['../assets/', '../../assets/', 'assets/']):
    """
    智能获取图片路径（尝试多个可能的相对路径）

    参数:
        relative_path: 相对路径，如 'sample-images/basic/landscape.jpg'
        attempts: 尝试的路径前缀列表

    返回:
        str: 找到的完整路径，如果都找不到返回None
    """
    for prefix in attempts:
        full_path = os.path.join(prefix, relative_path)
        if os.path.exists(full_path):
            return full_path
    return None


def load_image_or_exit(path, verbose=True):
    """
    加载图片，如果失败则退出程序

    参数:
        path: 图片路径
        verbose: 是否打印详细信息

    返回:
        img: 图片数组
    """
    img = imread_chinese(path)
    if img is None:
        if verbose:
            print(f"错误：无法读取图片！")
            print(f"路径: {path}")
            print(f"请检查文件是否存在")
        exit(1)
    if verbose:
        print(f"[OK] 图片读取成功: {os.path.basename(path)}")
    return img
