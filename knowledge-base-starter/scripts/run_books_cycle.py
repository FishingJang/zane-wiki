#!/usr/bin/env python3
from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
DEFAULT_SRC = ROOT / "raw" / "books"


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
    parser = argparse.ArgumentParser(description="Run a minimal books ingest cycle for PDF/EPUB knowledge-base inputs.")
    parser.add_argument("src", nargs="?", default=str(DEFAULT_SRC), help="Source directory containing PDF/EPUB files")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of book files processed (0 = all)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing extracted notes")
    parser.add_argument("--skip-report", action="store_true", help="Skip generating final health report")
    parser.add_argument("--allow-warn", action="store_true", help="Do not stop on lint/report warning exit codes")
    args = parser.parse_args()

    py = sys.executable
    src_dir = Path(args.src).expanduser().resolve()

    print()
    print("# Books Cycle")
    print(f"- source dir: {src_dir}")
    print(f"- limit: {args.limit}")
    print(f"- overwrite: {args.overwrite}")
    if not src_dir.exists():
        print("ERROR: source dir does not exist")
        raise SystemExit(2)
    print()

    extract_cmd = [py, str(SCRIPTS / "extract_books_to_notes.py"), "--src-dir", str(src_dir)]
    if args.limit > 0:
        extract_cmd.extend(["--limit", str(args.limit)])
    if args.overwrite:
        extract_cmd.append("--overwrite")
    run(extract_cmd, allow_fail=False)

    print()
    print("# Manual Agent Step Required")
    print("请在 raw/notes 更新后，使用 prompts/book-ingest-and-extract.md 驱动任意 Agent 执行 wiki 增量编译。")
    print("books 分支当前仍保留 Agent 语义编译步骤，因为它依赖章节抽象、概念归并、案例抽取与交叉链接判断。")
    print("注意：本脚本只适用于 PDF / EPUB / 书籍型资料。markdown / webclipper 资料请改走 scripts/run_ingest_cycle.py。")
    print()

    run([py, str(SCRIPTS / "kb_health_check.py")], allow_fail=args.allow_warn)
    run([py, str(SCRIPTS / "wiki_lint.py")], allow_fail=args.allow_warn)

    if not args.skip_report:
        run([py, str(SCRIPTS / "generate_ingest_report.py"), str(src_dir), "--batch", "custom", "--mode", "books-only"], allow_fail=args.allow_warn)
        run([py, str(SCRIPTS / "generate_health_report.py")], allow_fail=args.allow_warn)

    print()
    print("# Cycle Complete")
    print("- book extraction: done")
    print("- checks: done")
    print("- report: {}".format("skipped" if args.skip_report else "generated"))


if __name__ == "__main__":
    main()
