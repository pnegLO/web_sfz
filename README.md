# 证件照个性化处理平台

一个基于Flask和Vue.js的证件照处理系统，可以实现证件照换底色、裁剪成不同尺寸等功能。

## 项目特点

- 无需数据库，纯文件操作
- 简单易用的用户界面
- 支持多种证件照规格（一寸、二寸等）
- 多种背景颜色选择（红底、蓝底、白底、自定义颜色、自定义图片）
- 简单易部署，提供一键部署脚本

## 技术栈

- **前端**：Vue.js + Element UI
- **后端**：Flask + OpenCV/Python
- **图像处理**：OpenCV

## 功能列表

- 证件照背景色更换
  - 蓝底转红底/白底
  - 红底转蓝底/白底
  - 白底转红底/蓝底
  - 转换为自定义颜色
  - 转换为自定义背景图片
  - 支持马赛克背景
- 证件照尺寸裁剪
  - 一寸照片(25×35mm)
  - 二寸照片(35×49mm)
  - 小二寸照片(27×40mm)
  - 大一寸照片(33×48mm)
  - 小一寸照片(22×32mm)
  - 大二寸照片(35×53mm)

## 快速开始

### 一键部署

项目提供了一键部署脚本，只需运行：

```bash
python deploy.py
```

脚本会自动：
1. 检查Python环境
2. 安装所需依赖
3. 创建虚拟环境
4. 设置项目结构
5. 启动应用

### 手动部署

1. 安装依赖：
```bash
pip install flask opencv-python numpy pillow flask-cors
```

2. 启动应用：
```bash
python backend/app.py
```

3. 访问应用：
```
http://localhost:5000
```

## 项目结构

```
project/
│
├── backend/            # 后端代码
│   └── app.py          # Flask应用
│
├── frontend/           # 前端代码
│   ├── index.html      # 主页面
│   ├── css/            # 样式表
│   │   ├── main.css
│   │   └── variables.css
│   └── js/             # JavaScript脚本
│       ├── app.js      # Vue应用
│       ├── components.js # Vue组件
│       └── utils.js    # 工具函数
│
├── uploads/            # 上传图片存储目录
├── processed/          # 处理后图片存储目录
├── deploy.py           # 一键部署脚本
└── README.md           # 项目说明文档
```

## 使用案例

证件照处理平台适用于以下场景：
- 求职应聘需要准备各种尺寸的证件照
- 学校入学/注册需要特定底色的照片
- 证件办理需要符合特定规格的照片
- 快速批量处理多张证件照

## 开发者

**彭金 (PengJin)**
- 联系电话/微信：17-603603607

## 许可证

MIT 