from flask import Flask, request, jsonify, send_from_directory, Response
import os
import cv2
import numpy as np
import base64
from PIL import Image
import io
import uuid

app = Flask(__name__, static_folder='../frontend', static_url_path='')
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# 确保上传和处理文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def img_change_background(img, color):
    """将图像背景替换为指定颜色"""
    # 转换为RGB图像，如果是BGR格式
    if len(img.shape) == 3 and img.shape[2] == 3:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = img
        
    # 创建一个白色背景的遮罩
    mask = np.zeros(img_rgb.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # 定义前景区域
    rect = (10, 10, img_rgb.shape[1]-20, img_rgb.shape[0]-20)
    
    # 执行GrabCut算法分割图片
    cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    # 将可能是前景的区域标记为前景
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    
    # 解析颜色参数
    if color == 'red':
        bg_color = [255, 0, 0]  # 红色背景 RGB
    elif color == 'blue':
        bg_color = [0, 0, 255]  # 蓝色背景 RGB
    elif color == 'white':
        bg_color = [255, 255, 255]  # 白色背景 RGB
    else:
        # 解析自定义颜色，格式为 #RRGGBB
        try:
            if color.startswith('#'):
                color = color[1:]
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            bg_color = [r, g, b]
        except:
            # 默认为红色
            bg_color = [255, 0, 0]
    
    # 创建新的背景
    bg = np.zeros_like(img_rgb)
    bg[:] = bg_color
    
    # 合并前景和背景
    output = np.where(mask2[:, :, np.newaxis] == 1, img_rgb, bg)
    
    # 转回BGR格式用于OpenCV
    output_bgr = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    
    return output_bgr

@app.route('/')
def index():
    """提供前端页面"""
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理上传的图片文件"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    # 获取参数
    color = request.form.get('color', 'red')
    source_color = request.form.get('source_color', 'blue')
    size = request.form.get('size', 'original')
    
    # 处理自定义背景图
    bg_image_path = None
    if color == 'image' and 'bg_image' in request.files:
        bg_image = request.files['bg_image']
        if bg_image.filename != '':
            bg_image_filename = str(uuid.uuid4()) + os.path.splitext(bg_image.filename)[1]
            bg_image_path = os.path.join(UPLOAD_FOLDER, 'bg_' + bg_image_filename)
            bg_image.save(bg_image_path)

    # 生成唯一文件名
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    
    # 保存原始图片
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # 读取图片
    img = cv2.imread(file_path)
    if img is None:
        return jsonify({'error': '无法读取图片'}), 400

    try:
        # 处理图片
        if color == 'image' and bg_image_path:
            # 使用自定义背景图片
            result_img = img_change_background_with_image(img, bg_image_path)
        elif color == 'mosaic':
            # 使用马赛克背景
            result_img = img_change_background_mosaic(img)
        else:
            # 使用颜色背景
            result_img = img_change_background(img, color)
        
        # 如果选择了特定尺寸，裁剪图片
        if size != 'original':
            result_img = resize_to_standard(result_img, size)
        
        # 保存处理后的图片
        processed_path = os.path.join(PROCESSED_FOLDER, filename)
        cv2.imwrite(processed_path, result_img)
        
        # 返回成功信息
        return jsonify({
            'message': '图像处理成功',
            'original_path': file_path,
            'processed_path': processed_path,
            'filename': filename
        }), 200
    except Exception as e:
        return jsonify({'error': f'处理图片时出错: {str(e)}'}), 500

@app.route('/processed/<filename>')
def processed_file(filename):
    """提供处理后的图片下载"""
    # 使用绝对路径
    return send_from_directory(os.path.abspath(PROCESSED_FOLDER), filename)

@app.route('/original/<filename>')
def original_file(filename):
    """提供原始图片查看"""
    # 使用绝对路径
    return send_from_directory(os.path.abspath(UPLOAD_FOLDER), filename)

@app.after_request
def after_request(response):
    """配置CORS，允许跨域请求"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.after_request
def add_header(response):
    """添加调试信息到响应头"""
    print(f"请求路径: {request.path}, 状态码: {response.status_code}")
    return response

# 需要新增的辅助函数
def img_change_background_with_image(img, bg_image_path):
    """将图像背景替换为指定图片"""
    # 这里实现背景替换为自定义图片的逻辑
    bg_img = cv2.imread(bg_image_path)
    if bg_img is None:
        raise Exception("无法读取背景图片")
    
    # 调整背景图片大小为与原图相同
    bg_img = cv2.resize(bg_img, (img.shape[1], img.shape[0]))
    
    # 分割前景
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (10, 10, img.shape[1]-20, img.shape[0]-20)
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    
    # 合并前景和背景图片
    output = np.where(mask2[:, :, np.newaxis] == 1, img, bg_img)
    
    return output

def img_change_background_mosaic(img):
    """将图像背景替换为马赛克图案"""
    # 创建马赛克背景图案
    mosaic_size = 10
    mosaic_bg = np.zeros(img.shape, dtype=np.uint8)
    
    for y in range(0, img.shape[0], mosaic_size*2):
        for x in range(0, img.shape[1], mosaic_size*2):
            cv2.rectangle(mosaic_bg, (x, y), (x+mosaic_size, y+mosaic_size), (200, 200, 200), -1)
            cv2.rectangle(mosaic_bg, (x+mosaic_size, y+mosaic_size), 
                         (min(x+mosaic_size*2, img.shape[1]), min(y+mosaic_size*2, img.shape[0])), 
                         (150, 150, 150), -1)
    
    # 分割前景
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (10, 10, img.shape[1]-20, img.shape[0]-20)
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    
    # 合并前景和背景图案
    output = np.where(mask2[:, :, np.newaxis] == 1, img, mosaic_bg)
    
    return output

def resize_to_standard(img, size_key):
    """调整图片大小为标准证件照尺寸"""
    # 标准尺寸（宽x高，单位毫米，按照300dpi计算像素）
    size_map = {
        'one_inch': (295, 413),          # 25x35mm (1寸)
        'two_inch': (413, 579),          # 35x49mm (2寸)
        'large_one_inch': (390, 567),    # 33x48mm (大1寸)
        'small_one_inch': (260, 378),    # 22x32mm (小1寸)
        'large_two_inch': (413, 626),    # 35x53mm (大2寸)
        'small_two_inch': (320, 472),    # 27x40mm (小2寸)
    }
    
    if size_key not in size_map:
        return img
    
    target_width, target_height = size_map[size_key]
    
    # 裁剪为合适比例
    height, width = img.shape[:2]
    target_ratio = target_width / target_height
    current_ratio = width / height
    
    if current_ratio > target_ratio:
        # 图片太宽，需要裁剪宽度
        new_width = int(height * target_ratio)
        start_x = int((width - new_width) / 2)
        cropped = img[:, start_x:start_x+new_width]
    else:
        # 图片太高，需要裁剪高度
        new_height = int(width / target_ratio)
        start_y = int((height - new_height) / 2)
        cropped = img[start_y:start_y+new_height, :]
    
    # 调整到目标尺寸
    resized = cv2.resize(cropped, (target_width, target_height))
    
    return resized

if __name__ == '__main__':
    # 确保上传和处理文件夹存在并打印路径
    print(f"上传文件夹: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"处理文件夹: {os.path.abspath(PROCESSED_FOLDER)}")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 