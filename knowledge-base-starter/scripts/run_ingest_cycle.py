#!/usr/bin/env python3
from pathlib import Path
import argparse
import subprocess
import sys
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run(cmd, allow_fail=False):
    print("$", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print("stderr:")
        print(result.stderr.strip())
    if result.returncode != 0 and not allow_fail:
        raise SystemExit(result.returncode)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run a minimal ingest cycle for markdown/webclipper knowledge-base inputs.")
    parser.add_argument("src", help="Source directory containing markdown files")
    parser.add_argument("--date", default=date.today().isoformat(), help="Date prefix for raw ingest")
    parser.add_argument("--source", default="webclipper", help="Source label for raw ingest")
    parser.add_argument("--copy", action="store_true", help="Actually copy files into raw/articles")
    parser.add_argument("--skip-report", action="store_true", help="Skip generating final health report")
    parser.add_argument("--allow-warn", action="store_true", help="Do not stop on lint/report warning exit codes")
    args = parser.parse_args()

    py = sys.executable

    print("# Ingest Cycle")
    print(f"- source dir: {Path(args.src).expanduser().resolve()}")
    print(f"- date: {args.date}")
    print(f"- source label: {args.source}")
    print(f"- copy mode: {args.copy}")
    print()

    run([py, str(SCRIPTS / "ingest_raw_batch.py"), args.src, "--date", args.date, "--source", args.source] + (["--copy"] if args.copy else []), allow_fail=False)

    print()
    print("# Manual Agent Step Required")
    print("请在 raw 入库完成后，使用 prompts/knowledge-base-ingest-and-compile.md 驱动任意 Agent 执行 wiki 增量编译。")
    print("这一步是当前唯一仍未完全脚本化的步骤，因为它依赖主题提炼、概念归并和链接判断。")
    print("注意：本脚本只适用于 markdown / webclipper 输入。")
    print("如果输入是 PDF / EPUB / 书籍资料，不要调用本脚本；应改走 raw/books -> scripts/extract_books_to_notes.py -> prompts/book-ingest-and-extract.md 这条链路。")
    print()

    run([py, str(SCRIPTS / "kb_health_check.py")], allow_fail=args.allow_warn)
    run([py, str(SCRIPTS / "wiki_lint.py")], allow_fail=args.allow_warn)

    if not args.skip_report:
        run([py, str(SCRIPTS / "generate_ingest_report.py"), args.src, "--date", args.date, "--source", args.source, "--batch", "custom", "--mode", "articles-only"], allow_fail=args.allow_warn)
        run([py, str(SCRIPTS / "generate_health_report.py")], allow_fail=args.allow_warn)

    print()
    print("# Cycle Complete")
    print("- raw ingest: done")
    print("- checks: done")
    print("- report: {}".format("skipped" if args.skip_report else "generated"))


if __name__ == "__main__":
    main()
