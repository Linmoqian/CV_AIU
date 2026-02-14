# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是华南农业大学人工智能协会关于睿抗机器人培训会的OpenCV入门和简单图片处理培训项目，面向AI专业大一新生，通过4-6小时的短期课程让学生掌握OpenCV基础知识和图像处理基本技能。

## 项目结构

```
CV培训/
├── docs/                      # 教程文档（Markdown格式，按主题组织）
│   ├── 00-环境搭建.md
│   ├── 01-OpenCV简介与基础.md
│   └── ...
├── tasks/                     # 实践任务（包含README和评分标准）
│   ├── task-01/              # 任务1-5为基础练习
│   ├── task-02/
│   ├── task-03/
│   ├── task-04/
│   ├── task-05/
│   └── final-project/        # 期末考核项目（三选一）
├── src/                       # 示例代码
│   ├── examples/             # Python脚本版本示例（配合教程文档）
│   ├── notebooks/            # Jupyter Notebook版本（推荐用于学习）
│   ├── templates/            # 代码模板（ImageProcessor类）
│   └── utils/                # 工具库（display、image_helpers、io_helpers）
├── assets/                    # 图片资源
│   ├── sample-images/        # 测试图片（basic、colored-objects、noisy、shapes、real-world）
│   ├── test-videos/          # 测试视频
│   └── 生成测试图片.py        # 自动生成测试图片的脚本
└── README.md
```

## 核心架构

### 工具库设计 (`src/utils/`)

**display.py** - 图像显示辅助函数
- `show_image()` / `show_images()` - 使用matplotlib显示图像（自动BGR→RGB转换）
- `show_comparison()` - 创建并显示对比图
- `show_grid()` - 显示图像网格
- `create_comparison()` / `create_grid()` - 创建复合图像
- `show_histogram()` - 显示直方图
- `interactive_threshold()` - 交互式阈值调整

**image_helpers.py** - 图像处理辅助函数
- `load_image_or_exit()` - 加载图像失败则退出
- `save_image()` - 保存图像
- `resize_keep_aspect()` - 保持宽高比缩放
- `crop_center()` - 裁剪中心区域
- `add_watermark()` - 添加水印
- `auto_canny()` - 自动Canny边缘检测
- `sort_contours()` - 排序轮廓
- `adjust_brightness_contrast()` - 调整亮度和对比度
- `skeletonize()` - 骨架化

**io_helpers.py** - 中文路径处理
- `imread_chinese()` - 读取包含中文路径的图片（解决cv2.imread()不支持中文）
- `imwrite_chinese()` - 保存图片到中文路径
- `get_image_path()` - 智能获取图片路径（尝试多个相对路径）
- `load_image_or_exit()` - 加载图片失败则退出

### 代码模板 (`src/templates/`)

**ImageProcessor类** - 图像处理模板类
- 提供`load_image()`, `preprocess()`, `resize()`, `crop()`, `filter_blur()`, `detect_edges()`, `threshold()`, `extract_color()`, `morphology()`, `save()`, `show()`等方法
- 封装常用图像处理流程，适合快速开发

## 常用命令

### 环境配置
```bash
# 安装依赖（使用清华镜像加速）
pip install opencv-python numpy matplotlib jupyter -i https://pypi.tuna.tsinghua.edu.cn/simple

# 验证安装
python -c "import cv2; print(cv2.__version__)"
```

### 运行示例代码
```bash
# 方式1：运行Python脚本
python src/examples/01-read-display.py

# 方式2：启动Jupyter Notebook（推荐）
jupyter notebook
# 然后在浏览器中打开 src/notebooks/ 目录
```

### 生成测试图片
```bash
cd assets
python 生成测试图片.py
# 将在 assets/sample-images/ 目录下生成15张测试图片
```

### Jupyter Notebook操作
```bash
# 启动Jupyter
jupyter notebook

# 或使用JupyterLab
jupyter lab
```

在Notebook中:
- `Shift + Enter` - 运行当前单元格并跳到下一个
- `Ctrl + Enter` - 运行当前单元格
- `Cell` → `Run All` - 运行所有单元格

## 代码规范

### 文件路径处理
**重要：OpenCV的cv2.imread()和cv2.imwrite()不支持中文路径**

解决方法：
1. 使用`src/utils/io_helpers.py`中的工具函数
2. 或使用numpy的`fromfile()`和`imdecode()`：
   ```python
   img_array = np.fromfile(img_path, dtype=np.uint8)
   img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
   ```

### 图像显示
- **Python脚本**：使用`cv2.imshow()`, `cv2.waitKey(0)`, `cv2.destroyAllWindows()`
- **Jupyter Notebook**：使用matplotlib（cv2.imshow会导致问题）
  ```python
  import matplotlib.pyplot as plt
  plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
  plt.axis('off')
  plt.show()
  ```

### 代码结构
示例代码采用分段注释结构：
```python
# ==================== 1. 读取图像 ====================
print("1. 读取图像")
# ...代码

# ==================== 2. 查看属性 ====================
print("2. 图像属性")
# ...代码
```

### 图片保存
示例代码中的图片保存功能默认禁用，避免生成多余文件。如需保存，取消注释对应的`cv2.imwrite()`行。

## 学习路径

1. **环境搭建**：阅读`docs/00-环境搭建.md`，安装Python、OpenCV、Jupyter
2. **基础学习**：按顺序学习教程文档（01-08）和对应的示例代码
3. **实践任务**：完成`tasks/task-01/`到`tasks/task-05/`
4. **期末项目**：选择并完成`tasks/final-project/`中的项目（三选一）

## 图片资源说明

测试图片位于`assets/sample-images/`，分为5类：
- **basic/** - 基础图片（landscape.jpg, portrait.jpg, text.jpg）
- **colored-objects/** - 彩色物体（red-apple.jpg, blue-ball.jpg, mixed-colors.jpg）
- **noisy/** - 含噪图片（noisy-gaussian.jpg, noisy-salt-pepper.jpg）
- **shapes/** - 几何形状（coins.jpg, circles.jpg, rectangles.jpg）
- **real-world/** - 真实场景（document.jpg, license-plate.jpg, face.jpg）

使用相对路径`../../assets/sample-images/`或`../assets/`引用图片。

## Git工作流

- 每次更改需要提交PR，确保代码质量和项目结构清晰
- 代码应遵循PEP8规范
- 注释清晰，易于理解
- 避免提交生成的图片文件或临时输出

## 依赖包

- **opencv-python** - OpenCV主库
- **numpy** - 数组运算
- **matplotlib** - 图像显示（Jupyter Notebook必需）
- **jupyter** / **jupyterlab** - 交互式学习环境

## 常见问题

### 中文路径问题
所有代码都应使用`src/utils/io_helpers.py`中的工具函数处理中文路径。

### Notebook中cv2.imshow()失败
在Jupyter Notebook中必须使用matplotlib显示图像，cv2.imshow()会导致内核崩溃。

### 图片读取失败
检查：
1. 文件路径是否正确
2. 路径中是否包含中文（需用特殊方法处理）
3. 文件是否存在

### 保存图片功能被禁用
示例代码中`cv2.imwrite()`默认注释掉，避免生成多余文件。需要时取消注释即可。
