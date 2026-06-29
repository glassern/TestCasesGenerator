#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目管理工具
提供项目状态检查、清理、备份等功能
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import shutil
import zipfile

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))
from config import Config

class ProjectManager:
    """项目管理器"""
    
    def __init__(self):
        self.project_root = Config.PROJECT_ROOT
        self.output_dir = Config.OUTPUT_DIR
        self.product_dir = Config.PRODUCT_DIR
        
    def check_project_status(self):
        """检查项目状态"""
        print("🔍 检查项目状态...")
        print("="*50)
        
        status = {
            'directories': {},
            'files': {},
            'statistics': {}
        }
        
        # 检查目录
        directories_to_check = [
            ('product', self.product_dir),
            ('product/markdown', Config.MARKDOWN_DIR),
            ('product/modules', Config.MODULES_DIR),
            ('output', self.output_dir),
            ('script', Config.SCRIPT_DIR)
        ]
        
        for name, path in directories_to_check:
            exists = path.exists()
            status['directories'][name] = {
                'exists': exists,
                'path': str(path),
                'file_count': len(list(path.glob('*'))) if exists else 0
            }
            print(f"📁 {name}: {'✅' if exists else '❌'} ({status['directories'][name]['file_count']} 文件)")
        
        # 检查关键文件
        files_to_check = [
            ('config.py', self.project_root / 'config.py'),
            ('requirements.txt', self.project_root / 'requirements.txt'),
            ('README.md', self.project_root / 'README.md')
        ]
        
        for name, file_path in files_to_check:
            exists = file_path.exists()
            status['files'][name] = {
                'exists': exists,
                'path': str(file_path),
                'size': file_path.stat().st_size if exists else 0
            }
            print(f"📄 {name}: {'✅' if exists else '❌'}")
        
        # 统计信息
        if self.product_dir.exists():
            docx_files = list(self.product_dir.glob('*.docx'))
            md_files = list(Config.MARKDOWN_DIR.glob('*.md')) if Config.MARKDOWN_DIR.exists() else []
            status['statistics']['docx_count'] = len(docx_files)
            status['statistics']['markdown_count'] = len(md_files)
            print(f"📊 Word文档: {len(docx_files)} 个")
            print(f"📊 Markdown文档: {len(md_files)} 个")
        
        if self.output_dir.exists():
            json_files = list(self.output_dir.glob('*.json'))
            excel_files = list(self.output_dir.glob('*.xlsx'))
            status['statistics']['json_count'] = len(json_files)
            status['statistics']['excel_count'] = len(excel_files)
            print(f"📊 JSON文件: {len(json_files)} 个")
            print(f"📊 Excel文件: {len(excel_files)} 个")
        
        return status
    
    def clean_project(self, what='temp'):
        """清理项目文件"""
        print(f"🧹 清理项目文件: {what}")
        
        cleaned_files = []
        
        if what in ['temp', 'all']:
            # 清理临时文件
            temp_patterns = ['*.tmp', '*.temp', '*.log', '__pycache__']
            for pattern in temp_patterns:
                for file in self.project_root.rglob(pattern):
                    if file.is_file():
                        file.unlink()
                        cleaned_files.append(str(file))
                    elif file.is_dir() and pattern == '__pycache__':
                        shutil.rmtree(file)
                        cleaned_files.append(str(file))
        
        if what in ['output', 'all']:
            # 清理输出文件
            if self.output_dir.exists():
                for file in self.output_dir.glob('*'):
                    if file.is_file():
                        file.unlink()
                        cleaned_files.append(str(file))
        
        if what in ['markdown', 'all']:
            # 清理markdown文件
            if Config.MARKDOWN_DIR.exists():
                for file in Config.MARKDOWN_DIR.glob('*'):
                    if file.is_file():
                        file.unlink()
                        cleaned_files.append(str(file))
        
        print(f"✅ 清理完成，删除了 {len(cleaned_files)} 个文件")
        return cleaned_files
    
    def backup_project(self, backup_name=None):
        """备份项目"""
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_dir = self.project_root.parent / f"{self.project_root.name}_{backup_name}"
        
        print(f"💾 备份项目到: {backup_dir}")
        
        # 排除的目录和文件
        exclude_patterns = {
            '__pycache__', '.git', '.vscode', '.idea', 
            '*.tmp', '*.temp', '*.log'
        }
        
        def should_exclude(path):
            for pattern in exclude_patterns:
                if pattern in str(path) or path.name.startswith('.'):
                    return True
            return False
        
        # 复制项目文件
        copied_count = 0
        for item in self.project_root.rglob('*'):
            if should_exclude(item):
                continue
                
            relative_path = item.relative_to(self.project_root)
            backup_path = backup_dir / relative_path
            
            if item.is_file():
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, backup_path)
                copied_count += 1
            elif item.is_dir():
                backup_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ 备份完成，复制了 {copied_count} 个文件")
        return backup_dir
    
    def create_project_archive(self, archive_name=None):
        """创建项目压缩包"""
        if archive_name is None:
            archive_name = f"{self.project_root.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        
        archive_path = self.project_root.parent / archive_name
        
        print(f"📦 创建项目压缩包: {archive_path}")
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in self.project_root.rglob('*'):
                if file.is_file() and not any(exclude in str(file) for exclude in ['__pycache__', '.git', '*.tmp']):
                    arcname = file.relative_to(self.project_root.parent)
                    zipf.write(file, arcname)
        
        print(f"✅ 压缩包创建完成: {archive_path}")
        return archive_path
    
    def generate_project_report(self):
        """生成项目报告"""
        print("📊 生成项目报告...")
        
        status = self.check_project_status()
        
        report = {
            'project_name': self.project_root.name,
            'generated_at': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'status': status,
            'summary': {
                'total_directories': len(status['directories']),
                'valid_directories': sum(1 for d in status['directories'].values() if d['exists']),
                'total_files': len(status['files']),
                'valid_files': sum(1 for f in status['files'].values() if f['exists'])
            }
        }
        
        # 保存报告
        report_file = self.output_dir / f"project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Config.ensure_directories()  # 确保output目录存在
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 报告已保存: {report_file}")
        return report
    
    def run_maintenance(self):
        """运行维护任务"""
        print("🔧 运行项目维护...")
        print("="*50)
        
        # 1. 检查项目状态
        self.check_project_status()
        
        # 2. 清理临时文件
        print("\n🧹 清理临时文件...")
        self.clean_project('temp')
        
        # 3. 生成报告
        print("\n📊 生成维护报告...")
        self.generate_project_report()
        
        print("\n✅ 维护完成")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='智能三模块项目管理工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 状态检查
    subparsers.add_parser('status', help='检查项目状态')
    
    # 清理
    clean_parser = subparsers.add_parser('clean', help='清理项目文件')
    clean_parser.add_argument('what', choices=['temp', 'output', 'markdown', 'all'],
                             help='清理的内容类型')
    
    # 备份
    backup_parser = subparsers.add_parser('backup', help='备份项目')
    backup_parser.add_argument('--name', help='备份名称')
    
    # 压缩
    archive_parser = subparsers.add_parser('archive', help='创建项目压缩包')
    archive_parser.add_argument('--name', help='压缩包名称')
    
    # 报告
    subparsers.add_parser('report', help='生成项目报告')
    
    # 维护
    subparsers.add_parser('maintenance', help='运行维护任务')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    manager = ProjectManager()
    
    try:
        if args.command == 'status':
            manager.check_project_status()
        elif args.command == 'clean':
            manager.clean_project(args.what)
        elif args.command == 'backup':
            manager.backup_project(args.name)
        elif args.command == 'archive':
            manager.create_project_archive(args.name)
        elif args.command == 'report':
            manager.generate_project_report()
        elif args.command == 'maintenance':
            manager.run_maintenance()
        
        return 0
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        return 1

if __name__ == "__main__":
    exit(main())