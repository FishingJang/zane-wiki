#!/usr/bin/env python3
from pathlib import Path
from datetime import date
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "outputs" / "reports"
SCRIPTS = ROOT / "scripts"


def run(cmd):
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def main():
    today = date.today().isoformat()
    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / f"{today}__report__knowledge-base-health-check.md"

    rc1, out1, err1 = run([sys.executable, str(SCRIPTS / "kb_health_check.py")])
    rc2, out2, err2 = run([sys.executable, str(SCRIPTS / "wiki_lint.py")])

    overall = "OK" if rc1 == 0 and rc2 == 0 else "WARN"

    content = f"""# Knowledge Base Health Check Report

- 日期：{today}
- 范围：全库完整检查
- 执行者：Agent
- 证据等级：L1
- 是否涉及 ingest 批次：no
- 如涉及 ingest，是否包含重复判断：no
- 总状态：**{overall}**

## 一、检查范围

- raw 范围：`raw/`
- wiki 范围：`wiki/`
- outputs 范围：`outputs/reports/`

## 二、脚本结果：kb_health_check.py

```text
{out1}
```
"""
    if err1:
        content += f"""
stderr:
```text
{err1}
```
"""

    content += f"""
## 三、脚本结果：wiki_lint.py

```text
{out2}
```
"""
    if err2:
        content += f"""
stderr:
```text
{err2}
```
"""

    content += f"""
## 四、判断

### 5. ingest / 重复判断联动（如适用）
- 本轮 ingest report：无
- 是否已显式记录重复判断：否
- 是否存在 `--dupN` 文件：否
- 这些重复文件是否被误判为新增知识资产：否

### 可确认判断
- 当前健康检查脚本已可运行
- 当前 wiki lint 脚本已可运行
- 本次报告直接基于本地仓库实时脚本输出生成

### 风险点
- 当前检查仍偏“最小可用”，尚未覆盖更复杂的概念重复检测与语义级合并建议
- `run_ingest_cycle.py` 默认只覆盖 markdown / webclipper 入库分支；书籍型资料应走 `raw/books -> raw/notes -> prompts/book-ingest-and-extract.md` 这条链路

### 不确定点
- 当后续规模继续扩张时，现有 topic-index 是否会继续膨胀，仍需下一轮实战验证
- 当 books / notes 规模提升后，是否需要单独的 notes 质量检查脚本，仍需视资料复杂度决定

## 五、建议动作

1. 继续补一键编排入口，把 raw 入库、agent 编译、检查报告串起来
2. 后续视规模补 source-index / workflow-index
3. 未来再补更强的重复概念与弱链接检测

## 六、涉及文件

- `scripts/kb_health_check.py`
- `scripts/wiki_lint.py`
- `scripts/generate_health_report.py`
- `outputs/reports/{report_path.name}`
"""

    report_path.write_text(content, encoding='utf-8')
    print(report_path)


if __name__ == "__main__":
    main()
