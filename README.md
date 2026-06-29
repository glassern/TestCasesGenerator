# 智能测试用例生成工具

AI 驱动的测试用例生成系统，将产品需求文档自动转换为专业的 Excel 测试用例文件，并支持一键上传飞书。

## 功能特性

- 📄 支持飞书文档链接 / 本地 Word 文档作为输入
- 🤖 AI 自动分析文档结构，识别功能模块
- 🧪 12 维度测试覆盖（功能、场景、异常、边界、数据、UI、流程、权限、性能、兼容、安全、可用性）
- 📊 生成专业 Excel 测试用例（含 P1/P2/P3 等级、需求原文追溯）
- 📤 一键上传飞书在线表格，保留完整格式
- 🔄 支持大文档处理（3000+ 行智能分割）

## 环境准备

### 前置依赖

```bash
# Python 依赖
pip install -r requirements.txt

# Pandoc（仅本地 Word 文档需要）
brew install pandoc          # macOS
# sudo apt-get install pandoc  # Linux
```

### 配置飞书 MCP（读取飞书文档 & 上传必需）

```bash
amp mcp add lark-mcp -- npx -y @larksuiteoapi/lark-mcp mcp \
  -a <app_id> -s <app_secret> \
  --oauth --token-mode user_access_token
```

首次使用需完成 OAuth 登录：

```bash
npx -y @larksuiteoapi/lark-mcp login -a <app_id> -s <app_secret>
```

> Token 有效期约 2 小时，过期后重新执行登录命令即可。

### 检查环境

对 AI 说「检查依赖」，会自动检测并安装所有依赖项。

## 使用方式

### 方式一：飞书文档链接（推荐）

直接把飞书文档链接发给 AI，说「生成测试用例」：

```
https://xxx.feishu.cn/wiki/XxxTokenXxx
生成测试用例
```

### 方式二：本地 Word 文档

1. 将 `.docx` 文件放入 `product/` 目录
2. 对 AI 说「生成测试用例」

### 上传飞书

生成完成后，对 AI 说「上传」，即可自动上传到飞书在线表格。

### 重置目录

下次生成前，对 AI 说「重置」，会清理上一轮生成的所有文件。

## 目录结构

```
├── product/                   # 产品文档
│   ├── *.docx                # 原始 Word 文档
│   └── markdown/             # 转换后的 Markdown
├── output/                    # 生成的测试用例
│   ├── module_*.json         # 按模块分的 JSON 文件
│   └── *_测试用例_*.xlsx      # 最终 Excel 文件
├── script/                    # 核心脚本
│   ├── convert_docx_to_markdown.py
│   └── generate_final_excel.py
├── tools/                     # 可选工具
├── config.py                 # 配置管理
└── AGENTS.md                 # AI 规则体系
```

## 常用命令速查

| 指令 | 说明 |
|------|------|
| `生成测试用例` | 启动完整的三模块生成流程 |
| `上传` | 上传 Excel 到飞书在线表格 |
| `重置` | 清理生成文件，准备下一轮 |
| `检查依赖` | 检测并安装环境依赖 |
