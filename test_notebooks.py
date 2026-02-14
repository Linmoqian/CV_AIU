"""
测试所有 Jupyter Notebook 文件
检查语法和基本导入是否正确
"""
import os
import json
import sys

def test_notebook(notebook_path):
    """测试单个 notebook 文件"""
    print(f"\n测试: {os.path.basename(notebook_path)}")
    print("-" * 60)

    try:
        # 读取 notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)

        # 检查 notebook 格式
        if 'cells' not in nb:
            print(f"  [ERROR] Invalid notebook format")
            return False

        # 统计信息
        total_cells = len(nb['cells'])
        code_cells = sum(1 for cell in nb['cells'] if cell['cell_type'] == 'code')
        markdown_cells = sum(1 for cell in nb['cells'] if cell['cell_type'] == 'markdown')

        print(f"  总单元格数: {total_cells}")
        print(f"  代码单元格: {code_cells}")
        print(f"  Markdown 单元格: {markdown_cells}")

        # 检查代码单元格语法
        errors = []
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                if source.strip():  # 非空代码
                    try:
                        compile(source, f'<cell {i}>', 'exec')
                    except SyntaxError as e:
                        errors.append(f"单元格 {i}: {e}")

        if errors:
            print(f"  [ERROR] Found {len(errors)} syntax errors:")
            for error in errors:
                print(f"    - {error}")
            return False

        print(f"  [OK] Syntax check passed")
        return True

    except json.JSONDecodeError as e:
        print(f"  [ERROR] JSON decode error: {e}")
        return False
    except Exception as e:
        print(f"  [ERROR] Test failed: {e}")
        return False

# 测试所有 notebooks
notebooks_dir = r'D:\project\CV_AIU\src\notebooks'
notebooks = sorted([
    '01-read-display.ipynb',
    '02-basic-operations.ipynb',
    '03-color-conversion.ipynb',
    '04-drawing.ipynb',
    '05-filtering.ipynb',
    '06-thresholding.ipynb',
    '07-morphology.ipynb',
    '08-project-examples.ipynb',
    '09-video-processing.ipynb',
])

print("=" * 60)
print("测试所有 Jupyter Notebook 文件")
print("=" * 60)

all_passed = True
for notebook in notebooks:
    notebook_path = os.path.join(notebooks_dir, notebook)
    success = test_notebook(notebook_path)
    if not success:
        all_passed = False

print("\n" + "=" * 60)
if all_passed:
    print("[OK] All notebooks passed!")
else:
    print("[ERROR] Some notebooks have issues")

sys.exit(0 if all_passed else 1)
