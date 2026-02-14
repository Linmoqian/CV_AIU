# 睿抗机器人OpenCV培训

华南农业大学人工智能协会 - OpenCV图像处理入门培训

## 培训说明

本培训面向AI专业大一新生，旨在通过4-6小时的短期课程，让学生掌握OpenCV基础知识和图像处理基本技能，能够动手实践完成简单的视觉任务。

## 培训安排

### 第一次课（2.5小时）
- ✅ 环境搭建（15分钟）
- ✅ OpenCV基础：读取、显示、保存（30分钟）
- ✅ 图像基本操作：缩放、裁剪、翻转（45分钟）
- ✅ 色彩空间转换（30分钟）
- ✅ 绘制图形与文字（30分钟）

### 第二次课（2.5-3小时）
- ✅ 图像滤波（平滑、锐化）（45分钟）
- ✅ 边缘检测（30分钟）
- ✅ 图像阈值处理（30分钟）
- ✅ 形态学操作（30分钟）
- ✅ 综合实战项目（60-75分钟）

## 项目目录

```
CV培训/
├── docs/                      # 教程文档
│   ├── 00-环境搭建.md
│   ├── 01-OpenCV简介与基础.md
│   ├── 02-图像基本操作.md
│   ├── 03-色彩空间转换.md
│   ├── 04-图像绘制.md
│   ├── 05-图像滤波与增强.md
│   ├── 06-图像阈值处理.md
│   ├── 07-形态学操作.md
│   ├── 08-实战项目教程.md
│   └── 09-常见问题与调试技巧.md
│
├── tasks/                     # 实践任务
│   ├── task-01/              # 图像基本操作
│   ├── task-02/              # 色彩空间转换
│   ├── task-03/              # 图像滤波
│   ├── task-04/              # 边缘检测
│   ├── task-05/              # 颜色追踪
│   └── final-project/        # 期末考核项目（三选一）
│
├── src/                       # 示例代码
│   └── examples/             # 配合教程的示例代码
│       ├── 01-read-display.py
│       ├── 02-basic-operations.py
│       ├── 03-color-conversion.py
│       └── ...
│
└── assets/                    # 图片资源（待添加）
    ├── sample-images/
    │   ├── basic/            # 基础图片
    │   ├── colored-objects/  # 彩色物体
    │   ├── noisy/            # 含噪图片
    │   ├── shapes/           # 几何形状
    │   └── real-world/       # 真实场景
    └── test-videos/          # 测试视频
```

## 任务列表

### 课前准备
- [ ] 阅读 [00-环境搭建](./docs/00-环境搭建.md)
- [ ] 安装Python、OpenCV、Jupyter Notebook
- [ ] 运行测试代码验证安装

### 第一次课任务
- [ ] 完成 [Task 1: 图像基本操作](./tasks/task-01/README.md)
- [ ] 完成 [Task 2: 色彩空间转换](./tasks/task-02/README.md)

### 第二次课任务
- [ ] 完成 [Task 3: 图像滤波](./tasks/task-03/README.md)
- [ ] 完成 [Task 4: 边缘检测](./tasks/task-04/README.md)
- [ ] 完成 [Task 5: 颜色追踪](./tasks/task-05/README.md)

### 期末考核
- [ ] 选择并完成 [Final Project](./tasks/final-project/README.md)（三选一）
  - 项目A：智能文档扫描器
  - 项目B：颜色识别分类器
  - 项目C：简易美颜相机

## 考核方式

### 平时练习（40%）
- Task 1-5（每个8分）
- 评分：功能完成、代码质量、提交规范

### 期末项目（60%）
- 功能完整性：30分
- 代码质量：15分
- 技术报告：10分
- 创新性：5分

## 快速开始

### 1. 环境配置
```bash
pip install opencv-python numpy matplotlib jupyter -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 验证安装
```bash
python src/examples/01-read-display.py
```

### 3. 开始学习
从 [00-环境搭建](./docs/00-环境搭建.md) 开始，按顺序学习教程文档。

## 学习资源

- [OpenCV官方文档](https://docs.opencv.org/4.x/)
- [OpenCV Python教程](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- 教程文档位于 [docs/](./docs/) 目录

## 常见问题

详见 [09-常见问题与调试技巧](./docs/09-常见问题与调试技巧.md)

## 贡献指南

本培训项目持续完善中，欢迎提供反馈和建议！

