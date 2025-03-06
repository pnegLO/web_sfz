from tkinter import filedialog
from tkinter.tix import Tk

import numpy as np
import cv2

# 自定义路径保存修改后的图像
def save_image_with_dialog(img, title):
    # 打开“保存文件”对话框
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",  # 自动加上文件扩展名 .png
        title=title,  # 设置对话框标题
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]  # 允许保存为 PNG 或 JPEG 格式
    )
    # 检查用户是否选择了路径
    if save_path:
        cv2.imwrite(save_path, img)  # 保存图像到指定路径
        print(f'保存成功：{save_path}')
    else:
        print("未选择保存路径，未保存文件。")


# 背景蓝、白、红三色互换
# =========================================================================================================

# 定义 img_blue_to_red 函数
def img_blue_to_red(img):  # 蓝底转红底
    # 获取图像尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放图像
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 显示原图像
    cv2.imshow('Original Image', img)

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置蓝色的HSV阈值范围
    lower_blue = np.array([90, 70, 70])
    upper_blue = np.array([110, 255, 255])

    # 创建掩码，用于检测蓝色区域
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 在原图上将蓝色区域替换为红色
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 255:  # 如果掩码中的像素为白色
                img[i, j] = (0, 0, 255)  # 替换为红色 (BGR格式)

    # 显示修改后的图像
    cv2.imshow('Result Image', img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存红底图像")

    return img


# 定义 img_blue_to_white 函数
def img_blue_to_white(img):  # 蓝底转白底
    # 获取图像尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放图像
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 显示原图像
    cv2.imshow('Original Image', img)

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置蓝色的HSV阈值范围
    lower_blue = np.array([90, 70, 70])
    upper_blue = np.array([110, 255, 255])

    # 创建掩码，用于检测蓝色区域
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 在原图上将蓝色区域替换为白色
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 255:  # 如果掩码中的像素为白色
                img[i, j] = (255, 255, 255)  # 替换为白色 (BGR格式)

    # 显示修改后的图像
    cv2.imshow('Result Image', img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存白底图像")

    return img


# 定义 img_white_to_red 函数
def img_white_to_red(img):  # 白底转红底
    # 获取图像尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放图像
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 显示原图像
    cv2.imshow('Original Image', img)

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置白色的HSV阈值范围
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    # 创建掩码，用于检测白色区域
    mask = cv2.inRange(hsv, lower_white, upper_white)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 在原图上将蓝色区域替换为红色
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 255:  # 如果掩码中的像素为白色
                img[i, j] = (0, 0, 255)  # 替换为红色 (BGR格式)

    # 显示修改后的图像
    cv2.imshow('Result Image', img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存红底图像")

    return img


# 定义 img_white_to_blue 函数
def img_white_to_blue(img):  # 白底转蓝底
    # 获取图像尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放图像
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 显示原图像
    cv2.imshow('Original Image', img)

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置白色的HSV阈值范围
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    # 创建掩码，用于检测白色区域
    mask = cv2.inRange(hsv, lower_white, upper_white)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 在原图上将白色区域替换为蓝色
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 255:  # 如果掩码中的像素为白色
                img[i, j] = (219, 142, 67)  # 替换为蓝色 (BGR格式)

    # 显示修改后的图像
    cv2.imshow('Result Image', img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存蓝底图像")

    return img


# 定义 img_red_to_blue 函数
def img_red_to_blue(img):  # 红底转蓝底
    # 获取图像尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放图像
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 显示原图像
    cv2.imshow('Original Image', img)

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置红色的HSV阈值范围
    # lower_red = np.array([0, 100, 0])
    # upper_red = np.array([255, 255, 255])
    lower_red = np.array([0, 188, 183])
    upper_red = np.array([10, 255, 255])

    # 创建掩码，用于检测红色区域
    mask = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 在原图上将红色区域替换为蓝色
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 255:  # 如果掩码中的像素为白色
                img[i, j] = (219, 142, 67)  # 替换为蓝色 (BGR格式)

    # 显示修改后的图像
    cv2.imshow('Result Image', img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存蓝底图像")

    return img


# 定义 img_red_to_white 函数
def img_red_to_white(img):  # 红底转白底
    # 获取图像尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放图像
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 显示原图像
    cv2.imshow('Original Image', img)

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置红色的HSV阈值范围
    # lower_red = np.array([0, 100, 0])
    # upper_red = np.array([255, 255, 255])
    lower_red = np.array([0, 188, 183])
    upper_red = np.array([10, 255, 255])

    # 创建掩码，用于检测红色区域
    mask = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 在原图上将红色区域替换为白色
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 255:  # 如果掩码中的像素为白色
                img[i, j] = (255, 255, 255)  # 替换为白色 (BGR格式)

    # 显示修改后的图像
    cv2.imshow('Result Image', img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存白底图像")

    return img


# 自定义背景颜色
# =========================================================================================================

# 定义 img_blue_to_custom 函数，蓝底转自定义底色
def img_blue_to_custom(img, custom_color):  # 自定义颜色应为(B, G, R)格式
    # 获取图像尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放图像
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 显示原图像
    cv2.imshow('Original Image', img)

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置蓝色的HSV阈值范围
    lower_blue = np.array([90, 70, 70])
    upper_blue = np.array([110, 255, 255])

    # 创建掩码，用于检测蓝色区域
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作，消除噪点
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 在原图上将蓝色区域替换为自定义颜色
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 255:  # 如果掩码中的像素为白色，表示该区域是蓝色
                img[i, j] = custom_color  # 替换为自定义颜色

    # 显示修改后的图像
    cv2.imshow('Result Image', img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存自定义底色图像")

    return img


# 定义 img_white_to_custom 函数，白底转自定义底色
def img_white_to_custom(img, custom_color):  # 自定义颜色应为(B, G, R)格式
    # 获取图像尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放图像
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 显示原图像
    cv2.imshow('Original Image', img)

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置白色的HSV阈值范围
    # lower_white = np.array([0, 0, 200])
    # upper_white = np.array([180, 30, 255])
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 17, 255])

    # 创建掩码，用于检测白色区域
    mask = cv2.inRange(hsv, lower_white, upper_white)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作，消除噪点
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 在原图上将白色区域替换为自定义颜色
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 255:  # 如果掩码中的像素为白色，表示该区域是白色
                img[i, j] = custom_color  # 替换为自定义颜色

    # 显示修改后的图像
    cv2.imshow('Result Image', img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存自定义底色图像")

    return img


# 定义 img_red_to_custom 函数，红底转自定义底色
def img_red_to_custom(img, custom_color):  # 自定义颜色应为(B, G, R)格式
    # 获取图像尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放图像
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 显示原图像
    cv2.imshow('Original Image', img)

    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置红色的HSV阈值范围0,230,185
    lower_red = np.array([0, 188, 183])
    upper_red = np.array([10, 255, 255])

    # 创建掩码，用于检测红色区域
    mask = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作，消除噪点
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 在原图上将红色区域替换为自定义颜色
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] == 255:  # 如果掩码中的像素为白色，表示该区域是红色
                img[i, j] = custom_color  # 替换为自定义颜色

    # 显示修改后的图像
    cv2.imshow('Result Image', img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存自定义底色图像")

    return img


# 自定义背景图片
# ==========================================================================================================

# 定义 img_blue_to_diy_background 函数，蓝底转自定义背景图片
def img_blue_to_diy_background(img, background_img_path):
    # 获取原图尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放原图
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 读取自定义背景图片，并调整其大小与原图一致
    background_img = cv2.imread(background_img_path)
    background_img = cv2.resize(background_img, (cols, rows))

    # 显示原图像和背景图
    cv2.imshow('Original Image', img)
    cv2.imshow('Background Image', background_img)

    # 转换原图为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置蓝色的HSV阈值范围
    lower_blue = np.array([90, 70, 70])
    upper_blue = np.array([110, 255, 255])

    # 创建掩码，用于检测蓝色区域
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作，消除噪点
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 反转掩码（蓝色区域外的部分）
    mask_inv = cv2.bitwise_not(mask)

    # 将原图中的人物部分保留
    img_fg = cv2.bitwise_and(img, img, mask=mask_inv)

    # 将背景中的蓝色部分替换掉
    background_bg = cv2.bitwise_and(background_img, background_img, mask=mask)

    # 将图像与新背景合成
    result_img = cv2.add(img_fg, background_bg)

    # 显示修改后的图像
    cv2.imshow('Result Image', result_img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存自定义底色图片")

    return result_img


# 定义 img_white_to_diy_background 函数，白底转自定义背景图片
def img_white_to_diy_background(img, background_img_path):
    # 获取原图尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放原图
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 读取自定义背景图片，并调整其大小与原图一致
    background_img = cv2.imread(background_img_path)
    background_img = cv2.resize(background_img, (cols, rows))

    # 显示原图像和背景图
    cv2.imshow('Original Image', img)
    cv2.imshow('Background Image', background_img)

    # 转换原图为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置白色的HSV阈值范围
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 17, 255])

    # 创建掩码，用于检测白色区域
    mask = cv2.inRange(hsv, lower_white, upper_white)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作，消除噪点
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 反转掩码（白色区域外的部分）
    mask_inv = cv2.bitwise_not(mask)

    # 将原图中的人物部分保留
    img_fg = cv2.bitwise_and(img, img, mask=mask_inv)

    # 将背景中的白色部分替换掉
    background_bg = cv2.bitwise_and(background_img, background_img, mask=mask)

    # 将图像与新背景合成
    result_img = cv2.add(img_fg, background_bg)

    # 显示修改后的图像
    cv2.imshow('Result Image', result_img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存自定义底色图片")

    return result_img


# 定义 img_red_to_diy_background 函数，红底转自定义背景图片
def img_red_to_diy_background(img, background_img_path):
    # 获取原图尺寸
    rows, cols, channels = img.shape
    print(f'Original size: {rows}x{cols}, Channels: {channels}')

    # 缩放原图
    img = cv2.resize(img, None, fx=0.3, fy=0.3)
    rows, cols, channels = img.shape
    print(f'Resized size: {rows}x{cols}, Channels: {channels}')

    # 读取自定义背景图片，并调整其大小与原图一致
    background_img = cv2.imread(background_img_path)
    background_img = cv2.resize(background_img, (cols, rows))

    # 显示原图像和背景图
    cv2.imshow('Original Image', img)
    cv2.imshow('Background Image', background_img)

    # 转换原图为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('HSV Image', hsv)

    # 设置红色的HSV阈值范围
    lower_red = np.array([0, 188, 183])
    upper_red = np.array([10, 255, 255])

    # 创建掩码，用于检测红色区域
    mask = cv2.inRange(hsv, lower_red, upper_red)
    cv2.imshow('Blue Mask', mask)

    # 腐蚀和膨胀操作，消除噪点
    erosion = cv2.erode(mask, None, iterations=1)
    cv2.imshow('Erosion', erosion)

    dilation = cv2.dilate(mask, None, iterations=1)
    cv2.imshow('Dilation', dilation)

    # 反转掩码（红色区域外的部分）
    mask_inv = cv2.bitwise_not(mask)

    # 将原图中的人物部分保留
    img_fg = cv2.bitwise_and(img, img, mask=mask_inv)

    # 将背景中的红色部分替换掉
    background_bg = cv2.bitwise_and(background_img, background_img, mask=mask)

    # 将图像与新背景合成
    result_img = cv2.add(img_fg, background_bg)

    # 显示修改后的图像
    cv2.imshow('Result Image', result_img)

    # 调用保存图像对话框
    save_image_with_dialog(img, "保存自定义底色图片")

    return result_img


# 裁剪照片
# ========================================================================================================

# 按比例裁剪并保持人像居中
def crop_to_aspect(img, aspect_ratio):
    # 获取图像尺寸
    h, w, _ = img.shape

    # 计算目标尺寸
    target_h = h
    target_w = int(h * aspect_ratio)

    if target_w > w:
        target_w = w
        target_h = int(w / aspect_ratio)

    # 计算裁剪区域
    x_start = (w - target_w) // 2
    y_start = (h - target_h) // 2

    # 裁剪图像
    cropped_img = img[y_start:y_start + target_h, x_start:x_start + target_w]

    return cropped_img


# 定义一寸照的裁剪函数
def size_one_img(img):
    # 标准一寸照片比例为 295x413，宽高比为 295/413
    aspect_ratio = 295 / 413
    cropped_img = crop_to_aspect(img, aspect_ratio)

    # 调整为一寸照片尺寸
    resized_img = cv2.resize(cropped_img, (295, 413), interpolation=cv2.INTER_CUBIC)

    # 打印裁剪后的图像尺寸
    print(f"One Inch Photo Size: {resized_img.shape[1]}x{resized_img.shape[0]} pixels")

    return resized_img


# 定义二寸照的裁剪函数
def size_two_img(img):
    # 标准二寸照片比例为 413x626，宽高比为 413/626
    aspect_ratio = 413 / 626
    cropped_img = crop_to_aspect(img, aspect_ratio)

    # 调整为二寸照片尺寸
    resized_img = cv2.resize(cropped_img, (413, 626), interpolation=cv2.INTER_CUBIC)

    # 打印裁剪后的图像尺寸
    print(f"Two Inch Photo Size: {resized_img.shape[1]}x{resized_img.shape[0]} pixels")

    return resized_img


# 选择图片文件
def select_image_path():
    Tk().withdraw()
    return filedialog.askopenfilename(
        title="选择图片",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )


# 选择图片路径并读取图像
file_path = select_image_path()
if file_path:
    img = cv2.imread(file_path)
    if img is not None:
        # 调用蓝底转红底函数
        result_img = img_blue_to_red(img)

        # 使用该函数处理图像并自定义底色
        # 自定义颜色为(160, 32, 240) —— 紫色
        # custom_color = (124, 252, 0)

        # 固定底色转自定义底色
        # result_img = img_blue_to_custom(img, custom_color)

        # 使用该函数处理图像并替换背景
        # background_img_path = 'BJ1.jpg'  # 替换为自定义背景图路径

        # 调用函数，将蓝底换成自定义图片背景
        # result_img = img_blue_to_diy_background(img, background_img_path)

        # 调用一寸和二寸照片裁剪函数
        one_inch_photo = size_one_img(result_img)
        two_inch_photo = size_two_img(result_img)

        # 保存并显示一寸和二寸照片
        cv2.imshow('One Inch Photo', one_inch_photo)
        cv2.imshow('Two Inch Photo', two_inch_photo)

        # 使用 save_image_with_dialog 保存一寸和二寸照片
        save_image_with_dialog(one_inch_photo, "保存一寸照片")
        save_image_with_dialog(two_inch_photo, "保存二寸照片")

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("无法读取图片，请确认图片格式正确。")
else:
    print("未选择图片文件。")
