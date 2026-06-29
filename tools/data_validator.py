#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据校验和一致性检查工具
"""

import json
import os
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import Config

class DataValidator:
    """数据校验器"""
    
    def __init__(self):
        self.output_dir = Config.OUTPUT_DIR
        self.required_fields = Config.TEST_CASE_CONFIG['required_fields']
        self.valid_priorities = Config.TEST_CASE_CONFIG['priorities']
        self.validation_results = {
            'valid_files': [],
            'invalid_files': [],
            'warnings': [],
            'errors': []
        }
    
    def validate_json_file(self, file_path):
        """校验单个JSON文件"""
        print(f"🔍 校验文件: {file_path.name}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            return self._validate_json_structure(data, file_path)
            
        except json.JSONDecodeError as e:
            error_msg = f"JSON格式错误: 行{e.lineno}, 列{e.colno} - {e.msg}"
            self.validation_results['errors'].append(f"{file_path.name}: {error_msg}")
            return False
        except Exception as e:
            error_msg = f"文件读取错误: {e}"
            self.validation_results['errors'].append(f"{file_path.name}: {error_msg}")
            return False
    
    def _validate_json_structure(self, data, file_path):
        """校验JSON数据结构"""
        file_valid = True
        
        # 检查基本结构
        if not isinstance(data, dict):
            self.validation_results['errors'].append(f"{file_path.name}: 根对象必须是字典")
            return False
        
        # 检查test_cases字段
        if 'test_cases' not in data:
            self.validation_results['errors'].append(f"{file_path.name}: 缺少test_cases字段")
            return False
        
        test_cases = data['test_cases']
        if not isinstance(test_cases, list):
            self.validation_results['errors'].append(f"{file_path.name}: test_cases必须是数组")
            return False
        
        if len(test_cases) == 0:
            self.validation_results['warnings'].append(f"{file_path.name}: 测试用例为空")
        
        # 校验每个测试用例
        for i, test_case in enumerate(test_cases):
            case_valid = self._validate_test_case(test_case, file_path, i)
            if not case_valid:
                file_valid = False
        
        # 校验批次信息（如果存在）
        if 'batch_info' in data:
            self._validate_batch_info(data['batch_info'], file_path)
        
        return file_valid
    
    def _validate_test_case(self, test_case, file_path, index):
        """校验单个测试用例"""
        case_valid = True
        case_prefix = f"{file_path.name}[用例{index+1}]"
        
        # 检查必需字段
        for field in self.required_fields:
            if field not in test_case:
                self.validation_results['errors'].append(f"{case_prefix}: 缺少必需字段 '{field}'")
                case_valid = False
            elif not test_case[field] or str(test_case[field]).strip() == '':
                self.validation_results['errors'].append(f"{case_prefix}: 字段 '{field}' 不能为空")
                case_valid = False
        
        # 检查用例等级
        if '用例等级' in test_case:
            priority = test_case['用例等级']
            if priority not in self.valid_priorities:
                self.validation_results['errors'].append(
                    f"{case_prefix}: 无效的用例等级 '{priority}'，必须是 {self.valid_priorities} 之一"
                )
                case_valid = False
        
        # 检查用例名称重复
        case_name = test_case.get('用例名称', '')
        if case_name:
            self._check_duplicate_case_name(case_name, file_path, index)
        
        # 检查测试步骤格式
        test_steps = test_case.get('用例步骤', '')
        if test_steps:
            self._validate_test_steps(test_steps, case_prefix)
        
        return case_valid
    
    def _validate_batch_info(self, batch_info, file_path):
        """校验批次信息"""
        if not isinstance(batch_info, dict):
            self.validation_results['warnings'].append(f"{file_path.name}: batch_info应该是字典")
            return
        
        # 检查推荐字段
        recommended_fields = [
            'batch_number', 'total_batches', 'covered_modules', 
            'generation_time', 'test_dimensions_covered'
        ]
        
        for field in recommended_fields:
            if field not in batch_info:
                self.validation_results['warnings'].append(
                    f"{file_path.name}: 缺少推荐的batch_info字段 '{field}'"
                )
    
    def _check_duplicate_case_name(self, case_name, file_path, index):
        """检查重复的用例名称"""
        # 这里可以扩展为跨文件重复检查
        pass
    
    def _validate_test_steps(self, test_steps, case_prefix):
        """校验测试步骤格式"""
        # 检查是否包含编号步骤
        if not any(line.strip().startswith(f"{i}.") for i in range(1, 10) for line in test_steps.split('\n')):
            self.validation_results['warnings'].append(
                f"{case_prefix}: 测试步骤建议使用编号格式 (1. 2. 3. ...)"
            )
        
        # 检查步骤数量
        step_count = len([line for line in test_steps.split('\n') if line.strip().startswith(tuple(f"{i}." for i in range(1, 20)))])
        if step_count == 0:
            self.validation_results['warnings'].append(f"{case_prefix}: 测试步骤似乎没有明确的操作步骤")
        elif step_count > 15:
            self.validation_results['warnings'].append(f"{case_prefix}: 测试步骤过多({step_count}步)，建议简化")
    
    def validate_all_files(self):
        """校验所有测试用例文件"""
        print("🔍 开始数据校验...")
        
        # 查找所有JSON文件
        json_files = []
        for pattern in Config.SUPPORTED_JSON_FORMATS:
            json_files.extend(list(self.output_dir.glob(pattern)))
        
        if not json_files:
            print("❌ 未找到任何测试用例文件")
            return False
        
        print(f"📊 发现 {len(json_files)} 个文件需要校验")
        
        valid_count = 0
        for json_file in json_files:
            if self.validate_json_file(json_file):
                self.validation_results['valid_files'].append(json_file.name)
                valid_count += 1
            else:
                self.validation_results['invalid_files'].append(json_file.name)
        
        return valid_count == len(json_files)
    
    def check_data_consistency(self):
        """检查数据一致性"""
        print("\n🔍 检查数据一致性...")
        
        all_modules = set()
        all_case_names = set()
        duplicate_names = set()
        
        # 收集所有模块和用例名称
        for pattern in Config.SUPPORTED_JSON_FORMATS:
            for json_file in self.output_dir.glob(pattern):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    test_cases = data.get('test_cases', [])
                    for test_case in test_cases:
                        module = test_case.get('测试模块', '')
                        case_name = test_case.get('用例名称', '')
                        
                        if module:
                            all_modules.add(module)
                        
                        if case_name:
                            if case_name in all_case_names:
                                duplicate_names.add(case_name)
                            all_case_names.add(case_name)
                
                except Exception as e:
                    print(f"  ❌ 读取文件失败: {json_file.name} - {e}")
        
        # 报告重复的用例名称
        if duplicate_names:
            for name in duplicate_names:
                self.validation_results['warnings'].append(f"重复的用例名称: {name}")
        
        print(f"  📊 发现 {len(all_modules)} 个业务模块")
        print(f"  📊 发现 {len(all_case_names)} 个测试用例")
        if duplicate_names:
            print(f"  ⚠️  发现 {len(duplicate_names)} 个重复用例名称")
    
    def generate_validation_report(self):
        """生成校验报告"""
        report = {
            'validation_time': datetime.now().isoformat(),
            'summary': {
                'total_files': len(self.validation_results['valid_files']) + len(self.validation_results['invalid_files']),
                'valid_files': len(self.validation_results['valid_files']),
                'invalid_files': len(self.validation_results['invalid_files']),
                'warnings_count': len(self.validation_results['warnings']),
                'errors_count': len(self.validation_results['errors'])
            },
            'details': self.validation_results
        }
        
        # 保存报告
        report_file = self.output_dir / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 校验报告已保存: {report_file}")
        return report
    
    def print_summary(self):
        """打印校验摘要"""
        summary = self.validation_results
        
        print("\n" + "="*50)
        print("📊 数据校验摘要")
        print("="*50)
        
        print(f"✅ 有效文件: {len(summary['valid_files'])}")
        if summary['valid_files']:
            for file in summary['valid_files']:
                print(f"   - {file}")
        
        print(f"❌ 无效文件: {len(summary['invalid_files'])}")
        if summary['invalid_files']:
            for file in summary['invalid_files']:
                print(f"   - {file}")
        
        print(f"⚠️  警告: {len(summary['warnings'])}")
        if summary['warnings']:
            for warning in summary['warnings'][:5]:  # 只显示前5个
                print(f"   - {warning}")
            if len(summary['warnings']) > 5:
                print(f"   ... 还有 {len(summary['warnings']) - 5} 个警告")
        
        print(f"🚫 错误: {len(summary['errors'])}")
        if summary['errors']:
            for error in summary['errors'][:5]:  # 只显示前5个
                print(f"   - {error}")
            if len(summary['errors']) > 5:
                print(f"   ... 还有 {len(summary['errors']) - 5} 个错误")
        
        print("="*50)
    
    def run(self):
        """执行完整的校验流程"""
        print("🚀 开始数据校验和一致性检查...")
        
        # 校验所有文件
        all_valid = self.validate_all_files()
        
        # 检查数据一致性
        self.check_data_consistency()
        
        # 生成报告
        report = self.generate_validation_report()
        
        # 打印摘要
        self.print_summary()
        
        return all_valid and len(self.validation_results['errors']) == 0

def main():
    validator = DataValidator()
    success = validator.run()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())