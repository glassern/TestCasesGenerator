#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能三模块配置文件
"""

import os
from pathlib import Path

class Config:
    """配置管理类"""
    
    # 基础路径配置
    PROJECT_ROOT = Path(__file__).parent
    PRODUCT_DIR = PROJECT_ROOT / "product"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    SCRIPT_DIR = PROJECT_ROOT / "script"
    
    # 文档处理配置
    MARKDOWN_DIR = PRODUCT_DIR / "markdown"
    MODULES_DIR = PRODUCT_DIR / "modules"
    
    # 支持的文件格式
    SUPPORTED_DOCX_EXTENSIONS = ['.docx']
    SUPPORTED_JSON_FORMATS = ['module_*.json', 'batch_*.json']
    
    # Pandoc配置
    @classmethod
    def get_pandoc_options(cls):
        """获取Pandoc配置选项，使用动态路径"""
        media_path = cls.MARKDOWN_DIR / "media"
        return [
            '--wrap=none',  # 不自动换行
            f'--extract-media={media_path}'  # 提取图片（动态路径）
        ]
    
    # Excel配置
    EXCEL_CONFIG = {
        'columns': [
            '测试模块', '用例名称', '前置条件', '用例步骤', '预期结果', '用例等级',
            '开发验证人员', '冒烟测试结果', '测试人员', '测试结果-安卓', '测试结果-iOS', '备注'
        ],
        'column_widths': {
            'A': 15, 'B': 25, 'C': 20, 'D': 30, 'E': 25, 'F': 8,
            'G': 12, 'H': 12, 'I': 12, 'J': 12, 'K': 12, 'L': 15
        },
        'header_font': {'name': '微软雅黑', 'size': 12, 'bold': True},
        'cell_font': {'name': '微软雅黑', 'size': 10},
        'header_color': 'E6F2FF',
        'priority_colors': {
            'P1': 'FF0000',  # 红色
            'P2': '000000',  # 黑色
            'P3': '000000'   # 黑色
        }
    }
    
    # 文档分割配置
    DOCUMENT_SPLIT_CONFIG = {
        'max_lines': 2000,  # 超过此行数触发分割
        'min_module_lines': 100,  # 最小模块行数
        'exclude_patterns': [  # 排除的章节模式
            '修订记录', '版本历史', '变更日志', '文档说明',
            '需求概述', '项目背景', '术语定义'
        ]
    }
    
    # 测试用例生成配置
    TEST_CASE_CONFIG = {
        'dimensions': [  # 12个测试维度
            '功能覆盖', '场景覆盖', '异常覆盖', '边界覆盖',
            '数据覆盖', '界面覆盖', '流程覆盖', '权限覆盖',
            '性能覆盖', '兼容性覆盖', '安全覆盖', '可用性覆盖'
        ],
        'priorities': ['P1', 'P2', 'P3'],
        'required_fields': [
            '测试模块', '用例名称', '前置条件', '用例步骤', '预期结果', '用例等级'
        ]
    }
    
    # 错误处理配置
    ERROR_CONFIG = {
        'max_retries': 3,
        'retry_delay': 1,  # 秒
        'log_level': 'INFO',
        'error_log_file': OUTPUT_DIR / 'error.log'
    }
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        directories = [
            cls.PRODUCT_DIR,
            cls.OUTPUT_DIR,
            cls.MARKDOWN_DIR,
            cls.MODULES_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_env_config(cls, key, default=None):
        """获取环境变量配置"""
        return os.getenv(f"TESTGEN_{key}", default)
    
    @classmethod
    def update_config_from_env(cls):
        """从环境变量更新配置"""
        # 文档分割行数限制
        max_lines = cls.get_env_config('MAX_LINES')
        if max_lines and max_lines.isdigit():
            cls.DOCUMENT_SPLIT_CONFIG['max_lines'] = int(max_lines)
        
        # Excel文件名前缀
        excel_prefix = cls.get_env_config('EXCEL_PREFIX')
        if excel_prefix:
            cls.EXCEL_CONFIG['filename_prefix'] = excel_prefix
        
        # 日志级别
        log_level = cls.get_env_config('LOG_LEVEL')
        if log_level:
            cls.ERROR_CONFIG['log_level'] = log_level

# 初始化配置
Config.ensure_directories()
Config.update_config_from_env()