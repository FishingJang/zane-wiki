#!/usr/bin/env python3
from pathlib import Path
from datetime import date
import argparse
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "outputs" / "reports"
RAW_ARTICLES = ROOT / "raw" / "articles"
RAW_BOOKS = ROOT / "raw" / "books"
RAW_NOTES = ROOT / "raw" / "notes"


def list_markdown_files(src: Path):
    return sorted([p for p in src.glob("*.md") if p.is_file()])


def list_book_files(src: Path):
    return sorted([p for p in src.iterdir() if p.is_file() and p.suffix.lower() in {".pdf", ".epub"}])


def note_path_for_book(book: Path) -> Path:
    stem = book.name.lower()
    stem = re.sub(r"\.(pdf|epub)$", "", stem)
    stem = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "-", stem)
    stem = re.sub(r"-+", "-", stem).strip("-") or "untitled"
    return RAW_NOTES / f"extracted__{stem}.md"


def parse_extracted_chars(note_path: Path) -> int:
    if not note_path.exists():
        return 0
    text = note_path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"extracted_chars:\s*(\d+)", text)
    return int(match.group(1)) if match else 0


def build_articles_report(src: Path, report_path: Path, args) -> str:
    src_files = list_markdown_files(src)
    total_inputs = len(src_files)
    candidates = sorted(RAW_ARTICLES.glob(f"{args.date}__{args.source}__*.md"))
    matched_targets = []
    for file in src_files:
        matched = next((c for c in candidates if c.read_text(encoding='utf-8', errors='ignore') == file.read_text(encoding='utf-8', errors='ignore')), None)
        if matched:
            matched_targets.append(matched)

    return f"""# Knowledge Base Ingest Report

- 日期：{args.date}
- 批次：{args.batch}
- 来源目录：`{src}`
- 执行者：{args.executed_by}
- 处理模式：{args.mode}
- 是否启用重复判断：no

## 一、本轮输入概览
- 输入文件总数：{total_inputs}
- `.md / .html` 数量：{total_inputs}
- `.pdf / .epub` 数量：0
- 忽略资源文件 / sidecar 数量：0

## 二、路由结果
### 1. Articles 路径
- 新增到 `raw/articles/`：{len(matched_targets)}
- 因重复判断未继续升格：0
- 备注：当前为 markdown/webclipper 最小 ingest 报告，未自动执行重复语义判断

### 2. Books 路径
- 新增到 `raw/books/`：0
- 新增到 `raw/notes/`：0
- 提取失败 / 待补 OCR：0
- 备注：本轮不适用

### 3. 本轮未处理项
- 本轮无

## 三、重复判断总览
- `duplicate-source`：0
- `near-duplicate-topic`：0
- `book-duplicate-copy`：0
- `book-new-edition-candidate`：0
- `supplemental-source`：0
- 无重复命中：{total_inputs}

## 四、重复判断明细
> 当前脚本只生成最小模板占位；如本轮存在真实重复来源或近似重复材料，应由 ingest 执行者补全本段。

| 本次文件 | 命中对象 | 重复类型 | 本次动作 | 是否待重评 | 备注 |
| --- | --- | --- | --- | --- | --- |
| 本轮默认无 |  |  |  |  | 未启用自动重复判断 |

## 五、生命周期判断
- 新进入 `routed`：{len(matched_targets)}
- 新进入 `seeded`：0
- 保持 `parked`：0
- 新进入 `compiled`：0

## 六、可确认判断
- 本轮已完成最小 raw ingest 报告生成
- 当前报告基于源目录与 `raw/articles/` 实际落库结果生成
- 当前 runner 仍保留 Agent 语义编译步骤，不把 wiki 编译伪装成脚本自动化

## 七、风险点
- 当前脚本尚未自动识别近似重复主题，只输出最小 report 骨架
- 如果源文件被改名但内容重复，仍需人工或 Agent 补充重复判断

## 八、不确定点
- 是否需要把 slug 级命中、内容哈希比对、近似重复判断进一步脚本化，仍需后续真实批次验证

## 九、建议动作
1. 如本轮存在重复来源，请补全“重复判断总览”和“重复判断明细”
2. raw 入库后，继续用 `prompts/knowledge-base-ingest-and-compile.md` 驱动 Agent 做 wiki 编译
3. 完成 wiki 增量后，再跑 health report 形成闭环

## 十、涉及文件
- `{src}`
- `raw/articles/`
- `outputs/reports/{report_path.name}`
"""


def build_books_report(src: Path, report_path: Path, args) -> str:
    book_files = list_book_files(src)
    total_inputs = len(book_files)
    existing_books = [book for book in book_files if (RAW_BOOKS / book.name).exists()]
    note_files = [note_path_for_book(book) for book in book_files]
    note_exists = [note for note in note_files if note.exists()]
    weak_notes = [note for note in note_exists if parse_extracted_chars(note) < 2000]
    dup_books = [book for book in book_files if "--dup" in book.stem.lower()]

    return f"""# Knowledge Base Ingest Report

- 日期：{args.date}
- 批次：{args.batch}
- 来源目录：`{src}`
- 执行者：{args.executed_by}
- 处理模式：{args.mode}
- 是否启用重复判断：{'yes' if dup_books else 'no'}

## 一、本轮输入概览
- 输入文件总数：{total_inputs}
- `.md / .html` 数量：0
- `.pdf / .epub` 数量：{total_inputs}
- 忽略资源文件 / sidecar 数量：0

## 二、路由结果
### 1. Articles 路径
- 新增到 `raw/articles/`：0
- 因重复判断未继续升格：0
- 备注：本轮不适用

### 2. Books 路径
- 新增到 `raw/books/`：{len(existing_books)}
- 新增到 `raw/notes/`：{len(note_exists)}
- 提取失败 / 待补 OCR：{max(total_inputs - len(note_exists), 0)}
- 备注：字符数明显偏低的 notes 数量：{len(weak_notes)}

### 3. 本轮未处理项
- {'本轮无' if total_inputs == len(note_exists) else '存在未成功生成 notes 的书籍，需检查提取链路'}

## 三、重复判断总览
- `duplicate-source`：0
- `near-duplicate-topic`：0
- `book-duplicate-copy`：{len(dup_books)}
- `book-new-edition-candidate`：0
- `supplemental-source`：0
- 无重复命中：{max(total_inputs - len(dup_books), 0)}

## 四、重复判断明细
> books 分支当前只做最小重复信号记录；如需判断新版候选或补充来源，应由执行者补全本段。

| 本次文件 | 命中对象 | 重复类型 | 本次动作 | 是否待重评 | 备注 |
| --- | --- | --- | --- | --- | --- |
{chr(10).join([f'| {book.name} | 同名或重复副本候选 | `book-duplicate-copy` | `keep-raw-and-hold` | yes | 文件名含 --dup |' for book in dup_books]) or '| 本轮默认无 |  |  |  |  | 未命中 books 重复信号 |'}

## 五、生命周期判断
- 新进入 `routed`：{len(note_exists)}
- 新进入 `seeded`：0
- 保持 `parked`：{len(weak_notes)}
- 新进入 `compiled`：0

## 六、可确认判断
- 本轮已完成 books 分支最小 ingest 报告生成
- 当前报告基于 `raw/books/` 与 `raw/notes/` 的实际提取结果生成
- 当前 runner 仍保留 Agent 语义编译步骤，不把 books->wiki 编译伪装成脚本自动化

## 七、风险点
- 当前脚本尚未自动判断“疑似新版候选”和“有效补充来源”
- `extracted_chars` 偏低只能作为弱信号，不等于最终必须 parked

## 八、不确定点
- 是否需要把 OCR 质量阈值、版本差异比对、notes 质量复核进一步脚本化，仍需后续真实批次验证

## 九、建议动作
1. 如存在 `--dupN` 或明显低质量 notes，请补全“重复判断明细”和“生命周期判断”
2. notes 生成后，继续用 `prompts/book-ingest-and-extract.md` 驱动 Agent 做 wiki 编译
3. 完成 wiki 增量后，再跑 health report 形成闭环

## 十、涉及文件
- `{src}`
- `raw/books/`
- `raw/notes/`
- `outputs/reports/{report_path.name}`
"""


def main():
    parser = argparse.ArgumentParser(description="Generate a minimal ingest report for knowledge-base intake.")
    parser.add_argument("src", help="Source directory containing ingest files")
    parser.add_argument("--date", default=date.today().isoformat(), help="Date prefix for report naming")
    parser.add_argument("--source", default="webclipper", help="Source label for raw ingest")
    parser.add_argument("--mode", default="articles-only", choices=["articles-only", "books-only", "mixed"], help="Processing mode")
    parser.add_argument("--executed-by", default="Agent", help="Executor label")
    parser.add_argument("--batch", default="custom", help="Batch label, e.g. wave1 / mixed-ingest")
    args = parser.parse_args()

    src = Path(args.src).expanduser().resolve()
    if not src.exists() or not src.is_dir():
        print(f"ERROR: source directory not found: {src}")
        sys.exit(2)

    REPORTS.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS / f"{args.date}__report__knowledge-base-ingest.md"

    if args.mode == "books-only":
        content = build_books_report(src, report_path, args)
    else:
        content = build_articles_report(src, report_path, args)

    report_path.write_text(content, encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
