"""
视频处理模板
用于快速开始视频处理任务
"""

import cv2
import numpy as np
import time

class VideoProcessor:
    """视频处理类"""

    def __init__(self, source=0):
        """
        初始化

        参数:
            source: 视频源（摄像头索引或视频文件路径）
        """
        self.cap = cv2.VideoCapture(source)
        self.fps = 30
        self.width = 640
        self.height = 480
        self.writer = None

        if not self.cap.isOpened():
            print(f"错误: 无法打开视频源 {source}")
            return False

        # 获取视频属性
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS)) or 30
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"视频源打开成功")
        print(f"  分辨率: {self.width}x{self.height}")
        print(f"  帧率: {self.fps} FPS")

        return True

    def read_frame(self):
        """
        读取一帧

        返回:
            ret: 是否成功
            frame: 图像帧
        """
        ret, frame = self.cap.read()
        return ret, frame

    def preprocess_frame(self, frame):
        """
        预处理帧

        参数:
            frame: 输入帧

        返回:
            处理后的帧
        """
        # 转灰度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 高斯滤波
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        return blurred

    def process_frame(self, frame, processor_func=None):
        """
        处理帧（自定义处理函数）

        参数:
            frame: 输入帧
            processor_func: 处理函数

        返回:
            处理后的帧
        """
        if processor_func:
            return processor_func(frame)
        else:
            return frame

    def detect_edges(self, frame, threshold1=50, threshold2=150):
        """
        边缘检测

        参数:
            frame: 输入帧
            threshold1: 低阈值
            threshold2: 高阈值

        返回:
            边缘图像
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        return edges

    def extract_color(self, frame, color_name='red'):
        """
        颜色提取

        参数:
            frame: 输入帧
            color_name: 颜色名称

        返回:
            掩膜和结果帧
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 定义颜色范围（简化）
        colors = {
            'red': ([0, 100, 100], [10, 255, 255]),
            'green': ([35, 100, 100], [85, 255, 255]),
            'blue': ([85, 100, 100], [135, 255, 255])
        }

        if color_name not in colors:
            print(f"错误: 未知的颜色 {color_name}")
            return None, frame

        lower, upper = colors[color_name]
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

        # 形态学去噪
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # 应用掩膜
        result = cv2.bitwise_and(frame, frame, mask=mask)

        return mask, result

    def find_contours(self, mask, min_area=500):
        """
        查找轮廓

        参数:
            mask: 二值掩膜
            min_area: 最小面积

        返回:
            轮廓列表
        """
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        # 过滤小轮廓
        filtered = [c for c in contours if cv2.contourArea(c) > min_area]

        return filtered

    def draw_contours(self, frame, contours, color=(0, 255, 0), thickness=2):
        """
        绘制轮廓

        参数:
            frame: 输入帧
            contours: 轮廓列表
            color: 颜色
            thickness: 线宽

        返回:
            绘制后的帧
        """
        result = frame.copy()

        for contour in contours:
            # 获取边界框
            x, y, w, h = cv2.boundingRect(contour)

            # 绘制矩形
            cv2.rectangle(result, (x, y), (x + w, y + h), color, thickness)

            # 计算中心
            center_x = x + w // 2
            center_y = y + h // 2

            # 绘制中心点
            cv2.circle(result, (center_x, center_y), 5, color, -1)

        return result

    def setup_writer(self, output_path, fourcc='mp4v'):
        """
        设置视频写入器

        参数:
            output_path: 输出路径
            fourcc: 编码器
        """
        fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.writer = cv2.VideoWriter(output_path, fourcc,
                                     self.fps, (self.width, self.height))
        print(f"视频写入器已设置: {output_path}")

    def write_frame(self, frame):
        """
        写入帧

        参数:
            frame: 要写入的帧
        """
        if self.writer:
            self.writer.write(frame)

    def close_writer(self):
        """关闭写入器"""
        if self.writer:
            self.writer.release()
            print("视频写入完成")

    def process_video(self, processor_func=None, display=True,
                      save_output=False, output_path='output.mp4'):
        """
        处理整个视频

        参数:
            processor_func: 处理函数
            display: 是否显示
            save_output: 是否保存
            output_path: 输出路径
        """
        if save_output:
            self.setup_writer(output_path)

        frame_count = 0
        start_time = time.time()

        try:
            while True:
                ret, frame = self.cap.read()

                if not ret:
                    print("视频结束或无法读取帧")
                    break

                frame_count += 1

                # 处理帧
                if processor_func:
                    processed = processor_func(frame)
                else:
                    processed = frame

                # 显示
                if display:
                    # 添加帧数
                    display_frame = processed.copy()
                    cv2.putText(display_frame, f'Frame: {frame_count}',
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                               0.7, (0, 255, 0), 2)

                    cv2.imshow('Video Processing', display_frame)

                    # 按q退出
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                # 保存
                if save_output:
                    self.write_frame(processed)

        except KeyboardInterrupt:
            print("\n用户中断")

        finally:
            # 统计
            elapsed_time = time.time() - start_time
            if frame_count > 0:
                avg_fps = frame_count / elapsed_time
                print(f"\n处理完成:")
                print(f"  总帧数: {frame_count}")
                print(f"  耗时: {elapsed_time:.2f}秒")
                print(f"  平均FPS: {avg_fps:.2f}")

            self.close_writer()
            self.cap.release()
            cv2.destroyAllWindows()

    def release(self):
        """释放资源"""
        self.cap.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()


# ==================== 使用示例 ====================

def example_edge_detection(frame):
    """边缘检测示例"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # 转回BGR用于显示
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # 并排显示
    result = np.hstack([frame, edges_bgr])
    return cv2.resize(result, None, fx=0.5, fy=0.5)


def example_color_tracking(frame):
    """颜色追踪示例"""
    mask, result = VideoProcessor().extract_color(frame, 'red')

    if mask is not None:
        # 查找轮廓
        contours = VideoProcessor().find_contours(mask)

        # 绘制
        result = VideoProcessor().draw_contours(result, contours)

        # 并排显示
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        display = np.hstack([frame, result, mask_bgr])
        return cv2.resize(display, None, fx=0.5, fy=0.5)

    return frame


if __name__ == '__main__':
    import sys

    print("视频处理模板")
    print("=" * 50)

    if len(sys.argv) > 1:
        source = sys.argv[1]
        print(f"使用视频文件: {source}")
    else:
        source = 0
        print("使用摄像头")

    # 创建处理器
    processor = VideoProcessor(source)

    # 处理视频（取消注释想要的功能）

    # 1. 仅显示
    # processor.process_video(display=True, save_output=False)

    # 2. 边缘检测
    processor.process_video(processor_func=example_edge_detection,
                          display=True, save_output=False)

    # 3. 颜色追踪
    # processor.process_video(processor_func=example_color_tracking,
    #                       display=True, save_output=False)

    # 4. 保存处理结果
    # processor.process_video(processor_func=example_edge_detection,
    #                       display=True, save_output=True,
    #                       output_path='output.mp4')
