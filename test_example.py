"""
测试单个示例的核心功能（跳过GUI显示）
"""
import sys
import os

def test_example_file(example_file):
    """测试单个示例文件"""
    print(f"\nTesting: {os.path.basename(example_file)}")
    print("-" * 60)

    # 读取文件
    with open(example_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # 移除GUI相关代码
    lines = []
    skip_interactive = False
    indent_level = 0

    for line in code.split('\n'):
        # 检测交互式while True循环并跳过
        if 'while True:' in line and 'cv2.getTrackbarPos' in code[code.find(line):code.find(line)+500]:
            skip_interactive = True
            continue

        if skip_interactive:
            # 检测是否退出循环
            if line.strip() and not line.strip().startswith('#') and not line.startswith(' ' * (indent_level + 1)):
                skip_interactive = False
            else:
                continue

        # 跳过cv2.imshow调用
        if 'cv2.imshow' in line and not line.strip().startswith('#'):
            continue
        # 替换cv2.waitKey(0)为cv2.waitKey(1)
        if 'cv2.waitKey(0)' in line:
            line = line.replace('cv2.waitKey(0)', 'cv2.waitKey(1)')
        # 替换cv2.waitKey(2000)等
        if 'cv2.waitKey(' in line and not line.strip().startswith('#') and 'getTrackbarPos' not in line:
            line = line.replace('cv2.waitKey(', 'cv2.waitKey(1)  # Modified for test: cv2.waitKey(')
        # 保持其他代码不变
        lines.append(line)

    modified_code = '\n'.join(lines)

    # 添加cv2.destroyAllWindows以确保清理
    if 'cv2.destroyAllWindows()' not in modified_code:
        modified_code += '\ncv2.destroyAllWindows()\n'

    # 创建执行环境
    exec_globals = {
        '__name__': '__main__',
        '__file__': example_file,
        'cv2': __import__('cv2'),
        'np': __import__('numpy'),
        'os': os,
    }

    try:
        # 执行修改后的代码
        exec(compile(modified_code, example_file, 'exec'), exec_globals)
        print("[OK] Test passed")
        return True
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_example.py <example_file>")
        sys.exit(1)

    example_file = sys.argv[1]
    success = test_example_file(example_file)
    sys.exit(0 if success else 1)
