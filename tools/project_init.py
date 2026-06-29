#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目初始化工具
用于快速设置新的测试用例生成项目
"""

import os
import sys
from pathlib import Path
import shutil
import json

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))
from config import Config

class ProjectInitializer:
    """项目初始化器"""
    
    def __init__(self, project_name=None):
        self.project_name = project_name or "new_testcase_project"
        self.project_root = Path.cwd() / self.project_name
        
    def create_project_structure(self):
        """创建项目目录结构"""
        print(f"🚀 创建项目: {self.project_name}")
        
        # 创建基础目录
        directories = [
            self.project_root,
            self.project_root / "product",
            self.project_root / "product" / "markdown", 
            self.project_root / "product" / "modules",
            self.project_root / "output",
            self.project_root / "test_case",
            self.project_root / "script",
            self.project_root / ".cursor" / "rules"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  📁 创建目录: {directory.relative_to(Path.cwd())}")
            
        return True
    
    def copy_core_files(self):
        """复制核心文件"""
        print("\n📋 复制核心文件...")
        
        # 当前项目的根目录
        current_root = Path(__file__).parent.parent
        
        # 需要复制的文件
        files_to_copy = [
            ("script/convert_docx_to_markdown.py", "script/convert_docx_to_markdown.py"),
            ("script/generate_final_excel.py", "script/generate_final_excel.py"), 
            ("script/data_validator.py", "script/data_validator.py"),
            ("config.py", "config.py"),
            ("requirements.txt", "requirements.txt"),
            ("README.md", "README.md"),
            ("INSTALL.md", "INSTALL.md"),
            ("WORKFLOW.md", "WORKFLOW.md")
        ]
        
        for source_path, dest_path in files_to_copy:
            source = current_root / source_path
            destination = self.project_root / dest_path
            
            if source.exists():
                shutil.copy2(source, destination)
                print(f"  ✅ 复制: {dest_path}")
            else:
                print(f"  ❌ 源文件不存在: {source_path}")
        
        return True
    
    def copy_rules_system(self):
        """复制rules系统"""
        print("\n🤖 复制AI规则系统...")
        
        current_rules = Path(__file__).parent.parent / ".cursor" / "rules"
        target_rules = self.project_root / ".cursor" / "rules"
        
        if current_rules.exists():
            # 复制所有.mdc文件
            rule_files = list(current_rules.glob("*.mdc"))
            for rule_file in rule_files:
                destination = target_rules / rule_file.name
                shutil.copy2(rule_file, destination)
                print(f"  ✅ 复制规则: {rule_file.name}")
            
            # 复制README
            rules_readme = current_rules / "README.md"
            if rules_readme.exists():
                shutil.copy2(rules_readme, target_rules / "README.md")
                print(f"  ✅ 复制: rules/README.md")
        
        return True
    
    def create_example_files(self):
        """创建示例文件"""
        print("\n📝 创建示例文件...")
        
        # 创建示例配置文件
        example_config = {
            "project_name": self.project_name,
            "created_date": "2024-01-01",
            "description": "AI测试用例生成项目",
            "settings": {
                # 文档物理分割阈值：超过此行数时生成module_xx.md文件
                # 注意：无论是否分割，产品分析师模块都会执行结构分析
                "document_split_threshold": 2000,
                "excel_filename_template": "{product_name}_测试用例_{timestamp}.xlsx",
                "test_dimensions": 12
            }
        }
        
        config_file = self.project_root / "project_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(example_config, f, ensure_ascii=False, indent=2)
        print(f"  ✅ 创建: project_config.json")
        
        # 创建README模板
        readme_content = f"""# {self.project_name}

## 项目说明
这是一个基于智能三模块架构的AI测试用例生成项目。

## 快速开始
1. 将Word文档放入 `product/` 目录
2. 运行 `python script/convert_docx_to_markdown.py`
3. 与AI交互执行三模块流程
4. 运行 `python script/generate_final_excel.py`

## 项目结构
- `product/` - 产品文档目录
- `output/` - 输出结果目录  
- `script/` - 脚本文件目录
- `.cursor/rules/` - AI规则系统

## 相关文档
请参考根目录下的详细说明文档。
"""
        
        project_readme = self.project_root / "PROJECT_README.md"
        with open(project_readme, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  ✅ 创建: PROJECT_README.md")
        
        # 创建示例product说明
        product_readme = self.project_root / "product" / "README.md"
        with open(product_readme, 'w', encoding='utf-8') as f:
            f.write("""# 产品文档目录

## 使用说明
1. 将Word文档(.docx)放入此目录
2. 运行转换脚本生成Markdown文件
3. 开始AI三模块流程

## 目录结构
- `*.docx` - 原始Word文档
- `markdown/` - 转换后的Markdown文档
- `modules/` - 智能分割的模块文件（仅大文档>2000行时自动生成）
""")
        print(f"  ✅ 创建: product/README.md")
        
        return True
    
    def create_batch_scripts(self):
        """创建批处理脚本"""
        print("\n⚡ 创建便捷脚本...")
        
        # Windows批处理脚本
        windows_script = self.project_root / "run_conversion.bat"
        with open(windows_script, 'w', encoding='utf-8') as f:
            f.write("""@echo off
echo 运行Word文档转换...
python script/convert_docx_to_markdown.py
echo.
echo 转换完成！请继续AI三模块流程。
pause
""")
        print(f"  ✅ 创建: run_conversion.bat")
        
        windows_excel_script = self.project_root / "generate_excel.bat"
        with open(windows_excel_script, 'w', encoding='utf-8') as f:
            f.write("""@echo off
echo 生成Excel测试用例文件...
python script/generate_final_excel.py
echo.
echo Excel文件生成完成！
pause
""")
        print(f"  ✅ 创建: generate_excel.bat")
        
        # Linux/macOS脚本
        unix_script = self.project_root / "run_conversion.sh"
        with open(unix_script, 'w', encoding='utf-8') as f:
            f.write("""#!/bin/bash
echo "运行Word文档转换..."
python script/convert_docx_to_markdown.py
echo ""
echo "转换完成！请继续AI三模块流程。"
""")
        os.chmod(unix_script, 0o755)
        print(f"  ✅ 创建: run_conversion.sh")
        
        unix_excel_script = self.project_root / "generate_excel.sh"
        with open(unix_excel_script, 'w', encoding='utf-8') as f:
            f.write("""#!/bin/bash
echo "生成Excel测试用例文件..."
python script/generate_final_excel.py
echo ""
echo "Excel文件生成完成！"
""")
        os.chmod(unix_excel_script, 0o755)
        print(f"  ✅ 创建: generate_excel.sh")
        
        return True
    
    def create_gitignore(self):
        """创建.gitignore文件"""
        gitignore_content = """# 输出文件
output/*.xlsx
output/*.json
output/validation_report_*.json

# 临时文件
*.tmp
*.temp
.DS_Store
Thumbs.db

# Python缓存
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.pytest_cache/

# 虚拟环境
venv/
env/
.env

# IDE文件
.vscode/
.idea/
*.swp
*.swo

# 日志文件
*.log
error.log

# 媒体文件（如果不需要版本控制）
product/markdown/media/
"""
        
        gitignore_file = self.project_root / ".gitignore"
        with open(gitignore_file, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print(f"  ✅ 创建: .gitignore")
        
        return True
    
    def update_config_paths(self):
        """更新配置文件中的路径"""
        config_file = self.project_root / "config.py"
        
        if config_file.exists():
            # 读取配置文件内容
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换项目名称占位符
            content = content.replace('PROJECT_ROOT = Path(__file__).parent', 
                                    f'PROJECT_ROOT = Path(__file__).parent  # {self.project_name}')
            
            # 写回文件
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ 更新配置文件路径")
        
        return True
    
    def run(self):
        """执行完整的初始化流程"""
        print(f"🎯 初始化智能三模块项目: {self.project_name}")
        print("="*60)
        
        try:
            # 1. 创建目录结构
            if not self.create_project_structure():
                return False
            
            # 2. 复制核心文件
            if not self.copy_core_files():
                return False
            
            # 3. 复制rules系统
            if not self.copy_rules_system():
                return False
            
            # 4. 创建示例文件
            if not self.create_example_files():
                return False
            
            # 5. 创建批处理脚本
            if not self.create_batch_scripts():
                return False
            
            # 6. 创建.gitignore
            if not self.create_gitignore():
                return False
            
            # 7. 更新配置路径
            if not self.update_config_paths():
                return False
            
            print("\n" + "="*60)
            print("✅ 项目初始化完成！")
            print(f"📁 项目路径: {self.project_root}")
            print("\n🚀 下一步操作：")
            print(f"1. cd {self.project_name}")
            print("2. pip install -r requirements.txt")
            print("3. 将Word文档放入product/目录")
            print("4. python script/convert_docx_to_markdown.py")
            print("5. 开始AI三模块流程")
            
            return True
            
        except Exception as e:
            print(f"\n❌ 初始化失败: {e}")
            return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='智能三模块项目初始化工具')
    parser.add_argument('project_name', nargs='?', default='new_testcase_project',
                       help='项目名称 (默认: new_testcase_project)')
    parser.add_argument('--force', action='store_true',
                       help='强制覆盖已存在的项目')
    
    args = parser.parse_args()
    
    # 检查项目是否已存在
    project_path = Path.cwd() / args.project_name
    if project_path.exists() and not args.force:
        print(f"❌ 项目目录已存在: {project_path}")
        print("使用 --force 参数强制覆盖")
        return 1
    
    # 创建初始化器并运行
    initializer = ProjectInitializer(args.project_name)
    success = initializer.run()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())