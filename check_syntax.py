"""
检查所有示例脚本的语法
"""
import os
import glob
import py_compile

examples_dir = r'D:\project\CV_AIU\src\examples'

# 获取所有示例文件
example_files = sorted(glob.glob(os.path.join(examples_dir, '*.py')))

print("Checking syntax of all example scripts...")
print("="*60)

all_good = True
for file_path in example_files:
    filename = os.path.basename(file_path)
    try:
        py_compile.compile(file_path, doraise=True)
        print(f"[OK] {filename:30s} - Syntax OK")
    except py_compile.PyCompileError as e:
        print(f"[ERROR] {filename:30s} - Syntax Error")
        print(f"  {e}")
        all_good = False

print("="*60)
if all_good:
    print("[OK] All files passed syntax check!")
else:
    print("[ERROR] Some files have syntax errors")
