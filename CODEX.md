# Codex Usage

This project keeps the original Amp workflow intact. Codex should read and follow
`AGENTS.md` plus `.agents/skills/generating-testcases/SKILL.md` when generating
test cases. Do not change the test-case generation rules unless the user asks.

## Setup On A New Computer

Install Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Install Pandoc if you need to read local Word documents:

```bash
# macOS with Homebrew
brew install pandoc

# Or install from the official Pandoc release page:
# https://github.com/jgm/pandoc/releases
```

Check the local environment:

```bash
python3 codex.py check-local
```

Use `python3 codex.py check` only when you also want to inspect the original
Amp/Feishu MCP setup.

## Local Document Workflow

Use this path when you send Codex a local requirement document instead of a
Feishu link.

1. Put one or more `.docx` files in `product/`.
2. Convert Word documents to Markdown:

```bash
python3 codex.py convert
```

3. Ask Codex to generate test cases from the Markdown in `product/markdown/`.
   Codex must follow the original rules in `AGENTS.md` and
   `.agents/skills/generating-testcases/SKILL.md`.
4. After Codex writes `output/module_*.json`, build the final Excel file:

```bash
python3 codex.py excel
```

## Useful Commands

```bash
python3 codex.py status
python3 codex.py check-local
python3 codex.py reset
python3 codex.py reset --force
```

## Feishu Is Optional

If you provide local files directly to Codex, Feishu MCP and Amp OAuth are not
required. Feishu configuration is only needed for reading Feishu document links
or uploading Excel files back to Feishu.
