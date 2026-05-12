#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CHECK_SOURCE_DIRS = {"concepts", "topics", "cases"}
INDEX_TARGETS = {
    "topics": "topic-index.md",
    "cases": "topic-index.md",
}


def md_files(path: Path):
    return sorted(path.rglob("*.md")) if path.exists() else []


def check_short_pages(files):
    hits = []
    for file in files:
        text = file.read_text(encoding="utf-8", errors="ignore")
        lines = [x for x in text.splitlines() if x.strip()]
        if len(lines) < 8:
            hits.append((file, len(lines)))
    return hits


def check_duplicate_titles(files):
    title_map = {}
    duplicates = []
    for file in files:
        lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()
        title = next((line.strip() for line in lines if line.strip().startswith("# ")), None)
        if not title:
            continue
        if title in title_map:
            duplicates.append((title, title_map[title], file))
        else:
            title_map[title] = file
    return duplicates


def check_missing_source(files):
    hits = []
    for file in files:
        text = file.read_text(encoding="utf-8", errors="ignore")
        if file.parent.name in CHECK_SOURCE_DIRS:
            if "## 来源" not in text and "## Source" not in text:
                hits.append(file)
    return hits


def check_dead_links(files):
    hits = []
    for file in files:
        text = file.read_text(encoding="utf-8", errors="ignore")
        for match in LINK_RE.findall(text):
            if match.startswith("http://") or match.startswith("https://") or match.startswith("#"):
                continue
            target = (file.parent / match).resolve()
            if not target.exists():
                hits.append((file, match))
    return hits


def collect_index_reference_gaps(index_name: str, files):
    index_path = WIKI / "indexes" / index_name
    if not index_path.exists():
        return [f.name for f in files]
    text = index_path.read_text(encoding="utf-8", errors="ignore")
    missing = []
    for file in files:
        if file.name not in text:
            missing.append(file.name)
    return missing


def main():
    files = md_files(WIKI)
    scoped_files = []
    missing_in_indexes = {}
    for dirname, index_name in INDEX_TARGETS.items():
        dir_files = md_files(WIKI / dirname)
        scoped_files.extend(dir_files)
        missing_in_indexes[dirname] = collect_index_reference_gaps(index_name, dir_files)

    short_pages = check_short_pages(files)
    dup_titles = check_duplicate_titles(files)
    missing_source = check_missing_source(scoped_files + md_files(WIKI / "concepts"))
    dead_links = check_dead_links(files)

    print("# Wiki Lint Report")
    print()
    print("## Summary")
    print(f"- total wiki pages: {len(files)}")
    print(f"- short pages: {len(short_pages)}")
    print(f"- duplicate titles: {len(dup_titles)}")
    print(f"- missing source sections: {len(missing_source)}")
    print(f"- dead relative links: {len(dead_links)}")
    for dirname, index_name in INDEX_TARGETS.items():
        label = index_name.replace('.md', '')
        print(f"- {dirname} missing in {label}: {len(missing_in_indexes[dirname])}")
    print()

    if short_pages:
        print("## Short Pages")
        for file, line_count in short_pages[:20]:
            print(f"- {file}: non-empty lines={line_count}")
        print()

    if dup_titles:
        print("## Duplicate Titles")
        for title, first, second in dup_titles[:20]:
            print(f"- {title}: {first} <-> {second}")
        print()

    if missing_source:
        print("## Missing Source Sections")
        for file in missing_source[:20]:
            print(f"- {file}")
        print()

    if dead_links:
        print("## Dead Relative Links")
        for file, link in dead_links[:30]:
            print(f"- {file}: {link}")
        print()

    for dirname, index_name in INDEX_TARGETS.items():
        gaps = missing_in_indexes[dirname]
        if gaps:
            label = index_name.replace('.md', '')
            print(f"## {dirname.title()} Missing in {label}")
            for name in gaps[:20]:
                print(f"- {name}")
            print()

    problems = any([short_pages, dup_titles, missing_source, dead_links] + list(missing_in_indexes.values()))
    print(f"STATUS: {'WARN' if problems else 'OK'}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
