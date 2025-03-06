#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
证件照处理平台一键部署脚本
此脚本将检查环境、安装依赖、创建虚拟环境并启动应用
"""

import os
import sys
import platform
import subprocess
import shutil
import venv
import time
from pathlib import Path

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# 项目所需依赖
REQUIRED_PACKAGES = [
    'flask',
    'opencv-python',
    'numpy',
    'pillow',
    'flask-cors'
]

# 最低Python版本要求
MIN_PYTHON_VERSION = (3, 6)

def print_banner():
    """打印欢迎横幅"""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 80)
    print("                证件照处理平台 - 一键部署工具")
    print("=" * 80)
    print(f"{Colors.ENDC}")
    print(f"{Colors.BLUE}此脚本将帮助您设置并运行证件照处理平台。{Colors.ENDC}\n")

def check_python_installation():
    """检查Python是否已安装"""
    print(f"{Colors.BOLD}[1/6] 检查系统Python环境...{Colors.ENDC}")
    
    # 检查是否有pip可用
    pip_available = False
    try:
        subprocess.run(['pip', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pip_available = True
        print(f"  检测到pip已安装")
    except FileNotFoundError:
        print(f"  未检测到pip")
    
    if not pip_available:
        print(f"{Colors.YELLOW}警告: 未检测到pip，这可能影响依赖安装{Colors.ENDC}")
        choice = input(f"{Colors.YELLOW}是否尝试安装pip? (yes/no): {Colors.ENDC}")
        if choice.lower() in ['yes', 'y']:
            try:
                system = platform.system()
                if system == 'Windows':
                    print(f"  在Windows上安装pip...")
                    # 下载get-pip.py
                    subprocess.run(['curl', 'https://bootstrap.pypa.io/get-pip.py', '-o', 'get-pip.py'], check=True)
                    # 安装pip
                    subprocess.run([sys.executable, 'get-pip.py'], check=True)
                    # 清理下载文件
                    os.remove('get-pip.py')
                elif system == 'Linux':
                    print(f"  在Linux上安装pip...")
                    if shutil.which('apt'):
                        subprocess.run(['sudo', 'apt', 'update'], check=True)
                        subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-pip'], check=True)
                    elif shutil.which('yum'):
                        subprocess.run(['sudo', 'yum', 'install', '-y', 'python3-pip'], check=True)
                    else:
                        print(f"{Colors.RED}无法确定Linux发行版，请手动安装pip{Colors.ENDC}")
                        return False
                elif system == 'Darwin':  # macOS
                    print(f"  在macOS上安装pip...")
                    if shutil.which('brew'):
                        subprocess.run(['brew', 'install', 'python3'], check=True)
                    else:
                        print(f"  正在下载安装pip...")
                        subprocess.run(['curl', 'https://bootstrap.pypa.io/get-pip.py', '-o', 'get-pip.py'], check=True)
                        subprocess.run([sys.executable, 'get-pip.py'], check=True)
                        os.remove('get-pip.py')
                
                print(f"{Colors.GREEN}pip安装成功！{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}安装pip失败: {e}{Colors.ENDC}")
                print(f"{Colors.YELLOW}请手动安装pip后再运行此脚本{Colors.ENDC}")
                return False
    
    # 检查Python基础工具是否安装
    basic_packages = ['setuptools', 'wheel']
    missing_basic = []
    
    for package in basic_packages:
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'show', package], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
        except:
            missing_basic.append(package)
    
    if missing_basic:
        print(f"  缺少基础Python工具: {', '.join(missing_basic)}")
        choice = input(f"{Colors.YELLOW}是否安装这些基础工具? (yes/no): {Colors.ENDC}")
        if choice.lower() in ['yes', 'y']:
            try:
                print(f"  正在安装基础工具...")
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '--upgrade'] + missing_basic,
                    check=True
                )
                print(f"{Colors.GREEN}基础工具安装成功！{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}安装基础工具失败: {e}{Colors.ENDC}")
                return False
    
    print(f"{Colors.GREEN}Python环境检查完成！{Colors.ENDC}\n")
    return True

def check_python_version():
    """检查Python版本是否满足要求"""
    print(f"{Colors.BOLD}[2/6] 检查Python版本...{Colors.ENDC}")
    
    current_version = sys.version_info
    
    print(f"  当前Python版本: {sys.version.split()[0]}")
    print(f"  最低要求版本: {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}")
    
    if current_version < MIN_PYTHON_VERSION:
        print(f"{Colors.RED}错误：Python版本过低，请安装Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}或更高版本{Colors.ENDC}")
        choice = input(f"{Colors.YELLOW}是否尝试安装更新的Python版本? (yes/no): {Colors.ENDC}")
        if choice.lower() in ['yes', 'y']:
            try:
                system = platform.system()
                if system == 'Windows':
                    print(f"{Colors.YELLOW}Windows系统需要手动安装Python，请访问: https://www.python.org/downloads/{Colors.ENDC}")
                    print(f"{Colors.YELLOW}安装完成后，请重新运行此脚本{Colors.ENDC}")
                    sys.exit(1)
                elif system == 'Linux':
                    print(f"  在Linux上安装Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}...")
                    if shutil.which('apt'):
                        subprocess.run(['sudo', 'apt', 'update'], check=True)
                        subprocess.run(['sudo', 'apt', 'install', '-y', f'python{MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}'], check=True)
                    elif shutil.which('yum'):
                        subprocess.run(['sudo', 'yum', 'install', '-y', f'python{MIN_PYTHON_VERSION[0]}{MIN_PYTHON_VERSION[1]}'], check=True)
                    else:
                        print(f"{Colors.RED}无法确定Linux发行版，请手动安装Python{Colors.ENDC}")
                        sys.exit(1)
                elif system == 'Darwin':  # macOS
                    print(f"  在macOS上安装Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}...")
                    if shutil.which('brew'):
                        subprocess.run(['brew', 'install', f'python@{MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}'], check=True)
                    else:
                        print(f"{Colors.YELLOW}请先安装Homebrew，然后重新运行此脚本{Colors.ENDC}")
                        print(f"{Colors.YELLOW}安装Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"{Colors.ENDC}")
                        sys.exit(1)
                
                print(f"{Colors.GREEN}Python安装成功！请重新运行此脚本{Colors.ENDC}")
                sys.exit(0)
            except Exception as e:
                print(f"{Colors.RED}安装Python失败: {e}{Colors.ENDC}")
                sys.exit(1)
        else:
            sys.exit(1)
    
    print(f"{Colors.GREEN}Python版本检查通过！{Colors.ENDC}\n")
    return True

def check_dependencies(env_python=sys.executable):
    """检查所需依赖是否已安装"""
    print(f"{Colors.BOLD}[3/6] 检查项目依赖...{Colors.ENDC}")
    
    missing_packages = []
    
    # 使用pip列出已安装的包
    try:
        result = subprocess.run(
            [env_python, '-m', 'pip', 'freeze'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        installed = result.stdout.lower()
        
        for package in REQUIRED_PACKAGES:
            package_lower = package.lower().replace('-', '_')
            if package_lower not in installed:
                missing_packages.append(package)
    except subprocess.CalledProcessError:
        print(f"{Colors.RED}无法获取已安装的依赖列表{Colors.ENDC}")
        missing_packages = REQUIRED_PACKAGES
    
    if missing_packages:
        print(f"  缺少以下依赖:")
        for package in missing_packages:
            print(f"   - {package}")
        
        choice = input(f"\n{Colors.YELLOW}是否安装这些依赖? (yes/no): {Colors.ENDC}")
        if choice.lower() in ['yes', 'y']:
            try:
                print(f"  正在安装依赖...")
                for package in missing_packages:
                    print(f"   - 安装 {package}...")
                    subprocess.run(
                        [env_python, '-m', 'pip', 'install', package],
                        check=True
                    )
                print(f"{Colors.GREEN}所有依赖已成功安装！{Colors.ENDC}")
            except subprocess.CalledProcessError as e:
                print(f"{Colors.RED}安装依赖时出错: {e}{Colors.ENDC}")
                return False
        else:
            print(f"{Colors.YELLOW}警告: 缺少必要依赖，程序可能无法正常运行{Colors.ENDC}")
            return False
    else:
        print(f"{Colors.GREEN}所有依赖已满足！{Colors.ENDC}")
    
    print("")
    return True

def setup_virtual_env():
    """创建并激活虚拟环境"""
    print(f"{Colors.BOLD}[4/6] 设置虚拟环境...{Colors.ENDC}")
    
    venv_dir = Path("venv")
    
    # 检查虚拟环境是否已存在
    if venv_dir.exists():
        print(f"  发现已有虚拟环境")
        choice = input(f"{Colors.YELLOW}是否重新创建虚拟环境? (yes/no): {Colors.ENDC}")
        if choice.lower() in ['yes', 'y']:
            print(f"  正在删除旧的虚拟环境...")
            try:
                shutil.rmtree(venv_dir)
            except Exception as e:
                print(f"{Colors.RED}无法删除旧的虚拟环境: {e}{Colors.ENDC}")
                return None
        else:
            print(f"  使用现有虚拟环境")
            return get_venv_python_path(venv_dir)
    
    # 创建新的虚拟环境
    print(f"  创建新的虚拟环境...")
    try:
        venv.create(venv_dir, with_pip=True)
        print(f"{Colors.GREEN}虚拟环境创建成功！{Colors.ENDC}\n")
        return get_venv_python_path(venv_dir)
    except Exception as e:
        print(f"{Colors.RED}创建虚拟环境时出错: {e}{Colors.ENDC}")
        return None

def get_venv_python_path(venv_dir):
    """获取虚拟环境中的Python解释器路径"""
    if platform.system() == "Windows":
        return os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        return os.path.join(venv_dir, "bin", "python")

def setup_project_structure():
    """设置项目目录结构"""
    print(f"{Colors.BOLD}[5/6] 初始化项目结构...{Colors.ENDC}")
    
    # 确保必要的目录存在
    directories = [
        "frontend",
        "frontend/css",
        "frontend/js",
        "frontend/assets",
        "frontend/assets/images",
        "backend",
        "uploads",
        "processed"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  确保目录存在: {directory}")
    
    # 设置目录权限
    try:
        for directory in ["uploads", "processed"]:
            if platform.system() != "Windows":
                os.chmod(directory, 0o777)
                print(f"  设置目录权限: {directory}")
    except Exception as e:
        print(f"{Colors.YELLOW}警告: 无法设置目录权限: {e}{Colors.ENDC}")
    
    print(f"{Colors.GREEN}项目结构已初始化！{Colors.ENDC}\n")
    return True

def start_application(venv_python):
    """启动应用"""
    print(f"{Colors.BOLD}[6/6] 启动应用...{Colors.ENDC}")
    
    # 检查backend/app.py是否存在
    if not os.path.exists("backend/app.py"):
        print(f"{Colors.RED}错误：找不到应用程序入口，请确保 backend/app.py 文件存在{Colors.ENDC}")
        return False
    
    try:
        print(f"{Colors.GREEN}应用程序正在启动...{Colors.ENDC}")
        print(f"{Colors.YELLOW}按 Ctrl+C 可以停止应用{Colors.ENDC}")
        
        # 获取本地IP地址
        local_ip = get_local_ip()
        
        # 显示访问信息
        print(f"\n{Colors.BOLD}应用程序访问地址:{Colors.ENDC}")
        print(f"  本地访问: {Colors.GREEN}http://localhost:5000{Colors.ENDC}")
        if local_ip:
            print(f"  局域网访问: {Colors.GREEN}http://{local_ip}:5000{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}启动日志:{Colors.ENDC}")
        print("-" * 80)
        
        # 启动Flask应用
        subprocess.run(
            [venv_python, "backend/app.py"],
            check=True
        )
        
        return True
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}应用已停止{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.RED}启动应用时出错: {e}{Colors.ENDC}")
        return False

def get_local_ip():
    """获取本地IP地址"""
    import socket
    try:
        # 创建一个UDP套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个公共的DNS服务器，这里不会真的发送数据
        s.connect(("8.8.8.8", 80))
        # 获取分配的IP
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return None

def main():
    """主函数"""
    print_banner()
    
    # 检查Python安装
    if not check_python_installation():
        return
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 设置项目结构
    if not setup_project_structure():
        return
    
    # 设置虚拟环境
    venv_python = setup_virtual_env()
    if not venv_python:
        print(f"{Colors.RED}创建虚拟环境失败，使用当前Python环境继续{Colors.ENDC}")
        venv_python = sys.executable
    
    # 检查依赖
    if not check_dependencies(venv_python):
        print(f"{Colors.YELLOW}警告: 依赖检查未通过，程序可能无法正常运行{Colors.ENDC}")
        choice = input(f"{Colors.YELLOW}是否继续启动应用? (yes/no): {Colors.ENDC}")
        if choice.lower() not in ['yes', 'y']:
            print(f"{Colors.RED}部署中止{Colors.ENDC}")
            return
    
    # 等待1秒让用户看到结果
    time.sleep(1)
    
    # 启动应用
    start_application(venv_python)

if __name__ == "__main__":
    main() 