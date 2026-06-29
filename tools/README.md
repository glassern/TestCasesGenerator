# 辅助工具目录

这个目录包含可选的项目管理和维护工具，不属于核心测试用例生成流程。

## 工具列表

### 🔧 project_manager.py
项目管理工具，提供以下功能：
- `status` - 检查项目状态
- `clean` - 清理临时文件和输出文件
- `backup` - 备份项目
- `archive` - 创建项目压缩包
- `report` - 生成项目报告
- `maintenance` - 运行维护任务

**使用示例：**
```bash
python tools/project_manager.py status
python tools/project_manager.py clean temp
python tools/project_manager.py backup
```

### 🚀 project_init.py
项目初始化工具，用于创建新的测试用例生成项目。

**使用示例：**
```bash
python tools/project_init.py my_new_project
```

### ✅ data_validator.py
数据校验工具，用于验证生成的JSON测试用例文件。

**使用示例：**
```bash
python tools/data_validator.py
```

## 注意事项

- 这些工具是可选的，不影响核心的测试用例生成流程
- 核心流程只需要 `script/` 目录下的2个脚本
- 工具脚本可以根据需要使用，也可以完全忽略