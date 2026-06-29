#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word文档转Markdown工具
支持自动扫描product目录下的docx文件
"""

import subprocess
import sys
import os
import glob
import platform
from pathlib import Path

def check_pandoc():
    """检查pandoc是否已安装"""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def find_docx_files():
    """自动扫描product目录下的docx文件"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    product_dir = project_root / "product"
    
    if not product_dir.exists():
        print(f"错误: product目录不存在 - {product_dir}")
        return []
    
    # 搜索所有docx文件
    docx_pattern = str(product_dir / "*.docx")
    docx_files = glob.glob(docx_pattern)
    
    if not docx_files:
        print(f"提示: 在{product_dir}目录下未找到docx文件")
        return []
    
    print(f"🔍 发现 {len(docx_files)} 个Word文档:")
    for i, file in enumerate(docx_files, 1):
        print(f"  {i}. {os.path.basename(file)}")
    
    return docx_files

def convert_docx_to_markdown(docx_path, markdown_path=None):
    """将Word文档转换为Markdown格式"""
    
    # 如果没有指定输出路径，自动生成
    if markdown_path is None:
        # 获取文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(docx_path))[0]
        # 替换空格为下划线，保持中文字符
        clean_name = base_name.replace(' ', '_')
        # 创建输出目录（相对于项目根目录）
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        output_dir = os.path.join(project_root, "product", "markdown")
        os.makedirs(output_dir, exist_ok=True)
        markdown_path = os.path.join(output_dir, f"{clean_name}.md")
    
    try:
        print(f"🔄 开始转换: {os.path.basename(docx_path)}")
        
        # 动态获取Pandoc配置
        sys.path.append(os.path.dirname(script_dir))
        from config import Config
        pandoc_options = Config.get_pandoc_options()
        
        # 使用Pandoc进行转换，保留更多格式
        result = subprocess.run([
            'pandoc', 
            docx_path, 
            '-t', 'markdown',
            *pandoc_options,  # 使用动态配置
            '-o', markdown_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 转换成功: {markdown_path}")
            # 显示文件大小信息
            file_size = os.path.getsize(markdown_path)
            with open(markdown_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
            print(f"   文件大小: {file_size/1024:.1f}KB, 行数: {line_count}")
            return True
        else:
            print(f"❌ 转换失败: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ 错误: 未找到pandoc命令")
        print("请参考INSTALL.md安装pandoc")
        print(f"当前平台: {platform.system()}")
        if platform.system() == "Windows":
            print("Windows用户请检查pandoc是否添加到系统PATH")
        elif platform.system() == "Darwin":
            print("macOS用户可使用: brew install pandoc")
        elif platform.system() == "Linux":
            print("Linux用户可使用: sudo apt-get install pandoc")
        return False
    except PermissionError as e:
        print(f"❌ 权限错误: {e}")
        print("请检查文件和目录的读写权限")
        return False
    except UnicodeDecodeError as e:
        print(f"❌ 编码错误: {e}")
        print("请检查文档文件的字符编码")
        return False
    except Exception as e:
        print(f"❌ 转换过程中出错: {e}")
        print(f"错误类型: {type(e).__name__}")
        return False

def convert_all_docx():
    """转换所有找到的docx文件"""
    docx_files = find_docx_files()
    
    if not docx_files:
        return False
    
    success_count = 0
    total_count = len(docx_files)
    
    print(f"\n🚀 开始批量转换 {total_count} 个文档...")
    
    for docx_file in docx_files:
        if convert_docx_to_markdown(docx_file):
            success_count += 1
        print()  # 添加空行分隔
    
    print(f"📊 转换完成: {success_count}/{total_count} 成功")
    return success_count > 0

def main():
    print("📄 Word文档转Markdown工具")
    print("=" * 40)
    
    # 检查pandoc
    if not check_pandoc():
        print("❌ Pandoc未安装或不在PATH中")
        print("请参考INSTALL.md安装pandoc")
        sys.exit(1)
    
    # 如果提供了命令行参数，使用指定文件
    if len(sys.argv) >= 2:
        docx_path = sys.argv[1]
        markdown_path = sys.argv[2] if len(sys.argv) > 2 else None
        
        if not os.path.exists(docx_path):
            print(f"❌ 错误: 文件不存在 - {docx_path}")
            sys.exit(1)
        
        success = convert_docx_to_markdown(docx_path, markdown_path)
        sys.exit(0 if success else 1)
    
    # 自动模式：扫描并转换所有docx文件
    else:
        success = convert_all_docx()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 