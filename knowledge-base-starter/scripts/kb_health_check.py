#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"


def count_md(path: Path) -> int:
    return len(list(path.rglob("*.md"))) if path.exists() else 0


def count_files(path: Path, patterns) -> int:
    if not path.exists():
        return 0
    total = 0
    for pattern in patterns:
        total += len(list(path.rglob(pattern)))
    return total


def scan_line_number_pollution():
    hits = []
    if not WIKI.exists():
        return hits
    pattern = re.compile(r"^\s*\d+\|")
    for file in WIKI.rglob("*.md"):
        try:
            for i, line in enumerate(file.read_text(encoding="utf-8").splitlines(), start=1):
                if pattern.match(line):
                    hits.append((file, i, line[:120]))
        except Exception as e:
            hits.append((file, 0, f"READ_ERROR: {e}"))
    return hits


def has_text(path: Path, text: str) -> bool:
    return path.exists() and text in path.read_text(encoding="utf-8")


def main():
    topic_index = WIKI / "indexes" / "topic-index.md"
    current_focus = WIKI / "summaries" / "current-focus.md"
    overview = WIKI / "summaries" / "overview.md"
    investment_map = WIKI / "summaries" / "investment-map.md"

    raw_articles_count = count_md(RAW / "articles")
    raw_books_count = count_files(RAW / "books", ["*.pdf", "*.epub"])
    raw_notes_count = count_md(RAW / "notes")
    topic_count = count_md(WIKI / "topics")
    concept_count = count_md(WIKI / "concepts")
    case_count = count_md(WIKI / "cases")
    index_count = count_md(WIKI / "indexes")
    summary_count = count_md(WIKI / "summaries")

    pollution = scan_line_number_pollution()

    print("# Knowledge Base Health Check")
    print()
    print("## Counts")
    print(f"- raw articles: {raw_articles_count}")
    print(f"- raw books: {raw_books_count}")
    print(f"- raw notes: {raw_notes_count}")
    print(f"- topics: {topic_count}")
    print(f"- concepts: {concept_count}")
    print(f"- cases: {case_count}")
    print(f"- indexes: {index_count}")
    print(f"- summaries: {summary_count}")
    print()
    print("## Navigation Presence")
    print(f"- topic-index exists: {topic_index.exists()}")
    print(f"- current-focus exists: {current_focus.exists()}")
    print(f"- overview exists: {overview.exists()}")
    print(f"- investment-map exists: {investment_map.exists()}")
    print(f"- books layer exists: {(RAW / 'books').exists()}")
    print(f"- notes layer exists: {(RAW / 'notes').exists()}")
    print()
    print("## Minimal Link Checks")
    print(f"- topic-index references summary layer: {has_text(topic_index, 'overview.md') or has_text(topic_index, 'knowledge-base-ingestion-sop.md') or has_text(topic_index, 'current-focus.md')}")
    print(f"- overview references topic-index: {has_text(overview, 'topic-index')}")
    print()
    print("## Hygiene")
    print(f"- line-number-pollution hits: {len(pollution)}")
    if pollution:
        for file, line_no, text in pollution[:20]:
            print(f"  - {file}:{line_no}: {text}")
    print()

    if pollution:
        print("STATUS: WARN")
        sys.exit(1)
    else:
        print("STATUS: OK")


if __name__ == "__main__":
    main()
