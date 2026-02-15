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
OpenCV基础示例：图像的读取、显示和保存

学习目标:
    1. 掌握cv2.imread()读取图片
    2. 掌握cv2.imshow()显示图片
    3. 掌握cv2.imwrite()保存图片
"""

import cv2
import numpy as np
import os

# ==================== 1. 读取图像 ====================
print("1. 读取图像")

# 使用相对路径读取图片
script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, '../../assets/sample-images/basic/landscape.jpg')

# 检查文件是否存在
if not os.path.exists(img_path):
    print(f"错误：无法找到图片文件！")
    print(f"查找路径: {img_path}")
    print("请运行 'assets/生成测试图片.py' 生成测试图片")
    exit()

# 读取彩色图（默认）
# 使用np.fromfile解决中文路径问题
img_array = np.fromfile(img_path, dtype=np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

if img is None:
    print("错误：图片读取失败！")
    print("可能原因：路径包含中文字符")
    exit()

print(f"[OK] 图片读取成功: {os.path.basename(img_path)}")
print(f"    相对路径: assets/sample-images/basic/landscape.jpg")

# 读取灰度图（方法1：直接读取）
img_array = np.fromfile(img_path, dtype=np.uint8)
img_gray = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

# 读取灰度图（方法2：从彩色图转换）
img_gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ==================== 2. 查看图像属性 ====================
print("2. 图像属性")

print(f"图像形状: {img.shape}")
print(f"  - 高度: {img.shape[0]} 像素")
print(f"  - 宽度: {img.shape[1]} 像素")
print(f"  - 通道数: {img.shape[2]}")

print(f"\n图像尺寸: {img.size} 像素")
print(f"数据类型: {img.dtype}")

# ==================== 3. 访问像素 ====================
print("3. 像素访问")

# 访问单个像素（返回BGR值）
pixel = img[100, 100]
print(f"像素(100, 100)的BGR值: {pixel}")

# 访问单个通道
blue = img[100, 100, 0]
green = img[100, 100, 1]
red = img[100, 100, 2]
print(f"  B={blue}, G={green}, R={red}")

# ==================== 4. 显示图像 ====================
print("4. 显示图像")

# 显示彩色图
cv2.imshow('Color Image', img)

# 显示灰度图
cv2.imshow('Grayscale Image', img_gray)

# 等待按键（0表示无限等待）
print("按任意键关闭窗口...")
cv2.waitKey(0)

# 关闭所有窗口
cv2.destroyAllWindows()

# ==================== 5. 保存图像 ====================
print("5. 保存图像 (已禁用)")

# 保存功能已禁用，如需保存请取消以下注释
# cv2.imwrite('output_gray.jpg', img_gray)
# cv2.imwrite('output_gray.png', img_gray)
print("[提示] 图片保存功能已禁用，避免生成多余文件")

# ==================== 6. 创建测试图像 ====================
print("6. 创建测试图像")

# 创建一个300x300的蓝色图像
test_img = np.zeros((300, 300, 3), dtype=np.uint8)
test_img[:] = (255, 0, 0)  # BGR格式：蓝色

# 添加文字
cv2.putText(test_img, 'OpenCV Test', (50, 150),
           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

# 显示测试图像
cv2.imshow('Test Image', test_img)
cv2.waitKey(2000)  # 显示2秒后自动关闭
cv2.destroyAllWindows()

print("\n程序运行完成！")

# /**
#  *                                         ,s555SB@@&                          
#  *                                      :9H####@@@@@Xi                        
#  *                                     1@@@@@@@@@@@@@@8                       
#  *                                   ,8@@@@@@@@@B@@@@@@8                      
#  *                                  :B@@@@X3hi8Bs;B@@@@@Ah,                   
#  *             ,8i                  r@@@B:     1S ,M@@@@@@#8;                 
#  *            1AB35.i:               X@@8 .   SGhr ,A@@@@@@@@S                
#  *            1@h31MX8                18Hhh3i .i3r ,A@@@@@@@@@5               
#  *            ;@&i,58r5                 rGSS:     :B@@@@@@@@@@A               
#  *             1#i  . 9i                 hX.  .: .5@@@@@@@@@@@1               
#  *              sG1,  ,G53s.              9#Xi;hS5 3B@@@@@@@B1                
#  *               .h8h.,A@@@MXSs,           #@H1:    3ssSSX@1                  
#  *               s ,@@@@@@@@@@@@Xhi,       r#@@X1s9M8    .GA981               
#  *               ,. rS8H#@@@@@@@@@@#HG51;.  .h31i;9@r    .8@@@@BS;i;          
#  *                .19AXXXAB@@@@@@@@@@@@@@#MHXG893hrX#XGGXM@@@@@@@@@@MS        
#  *                s@@MM@@@hsX#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&,      
#  *              :GB@#3G@@Brs ,1GM@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@B,     
#  *            .hM@@@#@@#MX 51  r;iSGAM@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@8     
#  *          :3B@@@@@@@@@@@&9@h :Gs   .;sSXH@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:    
#  *      s&HA#@@@@@@@@@@@@@@M89A;.8S.       ,r3@@@@@@@@@@@@@@@@@@@@@@@@@@@r    
#  *   ,13B@@@@@@@@@@@@@@@@@@@5 5B3 ;.         ;@@@@@@@@@@@@@@@@@@@@@@@@@@@i    
#  *  5#@@#&@@@@@@@@@@@@@@@@@@9  .39:          ;@@@@@@@@@@@@@@@@@@@@@@@@@@@;    
#  *  9@@@X:MM@@@@@@@@@@@@@@@#;    ;31.         H@@@@@@@@@@@@@@@@@@@@@@@@@@:    
#  *   SH#@B9.rM@@@@@@@@@@@@@B       :.         3@@@@@@@@@@@@@@@@@@@@@@@@@@5    
#  *     ,:.   9@@@@@@@@@@@#HB5                 .M@@@@@@@@@@@@@@@@@@@@@@@@@B    
#  *           ,ssirhSM@&1;i19911i,.             s@@@@@@@@@@@@@@@@@@@@@@@@@@S   
#  *              ,,,rHAri1h1rh&@#353Sh:          8@@@@@@@@@@@@@@@@@@@@@@@@@#:  
#  *            .A3hH@#5S553&@@#h   i:i9S          #@@@@@@@@@@@@@@@@@@@@@@@@@A. 
#  *
#  *
#  *    又看源码！
#  */