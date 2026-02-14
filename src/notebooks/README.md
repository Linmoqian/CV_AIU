# Jupyter Notebook 示例

本目录包含所有OpenCV示例的Jupyter Notebook版本。

## 为什么使用 Jupyter Notebook？

Jupyter Notebook 是学习OpenCV的理想工具，提供：

- **交互式学习**：逐步执行代码，观察每步结果
- **即时可视化**：图像直接显示在notebook中，无需打开新窗口
- **实时修改**：可以修改代码并立即重新运行
- **文档结合**：代码和解释在同一文档中
- **适合教学**：讲师演示时更加直观

## 使用方法

### 1. 启动 Jupyter Notebook

```bash
# 在项目根目录运行
jupyter notebook

# 或使用 JupyterLab（推荐）
jupyter lab
```

### 2. 打开 Notebook

在浏览器中：
1. 导航到 `src/notebooks/` 目录
2. 选择对应的 `.ipynb` 文件
3. 点击运行

### 3. 运行代码

- **运行单个单元格**：选中单元格，按 `Shift + Enter`
- **运行所有单元格**：菜单栏选择 `Cell` → `Run All`
- **停止运行**：按 `Ctrl + C` 或点击停止按钮

## Notebook 列表

| # | Notebook | 内容 | 预计时间 |
|---|----------|------|---------|
| 1 | [01-read-display.ipynb](./01-read-display.ipynb) | 图像读取、显示与保存 | 20分钟 |
| 2 | [02-basic-operations.ipynb](./02-basic-operations.ipynb) | 图像基本操作（缩放、裁剪、翻转、旋转） | 30分钟 |
| 3 | [03-color-conversion.ipynb](./03-color-conversion.ipynb) | 色彩空间转换与颜色提取 | 25分钟 |
| 4 | [04-drawing.ipynb](./04-drawing.ipynb) | 绘制图形与文字 | 20分钟 |
| 5 | [05-filtering.ipynb](./05-filtering.ipynb) | 图像滤波与边缘检测 | 30分钟 |
| 6 | [06-thresholding.ipynb](./06-thresholding.ipynb) | 图像阈值处理 | 20分钟 |
| 7 | [07-morphology.ipynb](./07-morphology.ipynb) | 形态学操作 | 25分钟 |
| 8 | [08-project-examples.ipynb](./08-project-examples.ipynb) | 综合实战项目 | 40分钟 |
| 9 | [09-video-processing.ipynb](./09-video-processing.ipynb) | 视频处理基础 | 30分钟 |

## 注意事项

### 中文路径问题

项目已包含中文路径处理工具，所有notebook都可以正常读取中文路径的图片。

### 图像显示

Notebook中使用 `cv2.imshow()` 会导致问题，我们已将所有示例改为使用 Matplotlib 显示：

```python
# 使用 matplotlib 显示
import matplotlib.pyplot as plt
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
```

### 保存图片

示例代码中的图片保存功能已禁用，如需保存请取消注释对应的 `cv2.imwrite()` 行。

## 与 Python 脚本的对比

| 特性 | Python脚本 | Jupyter Notebook |
|------|-----------|------------------|
| 运行方式 | 终端命令 | 浏览器界面 |
| 代码执行 | 一次性运行全部 | 逐步执行单元格 |
| 结果显示 | 弹出新窗口 | 内嵌显示 |
| 适合场景 | 生产环境、批处理 | 学习、实验、演示 |
| 代码修改 | 需要重新运行 | 实时修改和运行 |

## 学习建议

1. **按顺序学习**：从 01 开始，按顺序完成所有notebook
2. **动手实践**：不要只运行代码，尝试修改参数观察效果
3. **添加笔记**：在notebook中添加自己的笔记和注释
4. **实验探索**：复制单元格进行实验，探索OpenCV的各种功能
5. **保存进度**：运行后notebook会保存输出结果，方便复习

## 常见问题

### Q: 图像显示不出来？
A: 确保在代码单元格中导入了matplotlib：`import matplotlib.pyplot as plt`

### Q: 如何重启内核？
A: 菜单栏选择 `Kernel` → `Restart`

### Q: 如何清除所有输出？
A: 菜单栏选择 `Cell` → `All Output` → `Clear`

### Q: Notebook无法打开？
A: 确保已安装Jupyter：`pip install jupyter`

## 进阶学习

完成所有notebook后，可以：
1. 尝试修改代码实现新功能
2. 完成tasks目录下的实践任务
3. 完成final-project的期末项目
4. 阅读OpenCV官方文档深入学习

## 反馈与建议

如有问题或建议，欢迎反馈！
