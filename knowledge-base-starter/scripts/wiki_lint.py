#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


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
        if file.parent.name in {"concepts", "topics"}:
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


def topic_index_refs_all_topics(files):
    topic_index = WIKI / "indexes" / "topic-index.md"
    if not topic_index.exists():
        return [f.name for f in files]
    text = topic_index.read_text(encoding="utf-8", errors="ignore")
    missing = []
    for file in files:
        if file.name not in text:
            missing.append(file.name)
    return missing


def main():
    files = md_files(WIKI)
    topic_files = md_files(WIKI / "topics")
    concept_files = md_files(WIKI / "concepts")

    short_pages = check_short_pages(files)
    dup_titles = check_duplicate_titles(files)
    missing_source = check_missing_source(topic_files + concept_files)
    dead_links = check_dead_links(files)
    missing_topics_in_index = topic_index_refs_all_topics(topic_files)

    print("# Wiki Lint Report")
    print()
    print("## Summary")
    print(f"- total wiki pages: {len(files)}")
    print(f"- short pages: {len(short_pages)}")
    print(f"- duplicate titles: {len(dup_titles)}")
    print(f"- missing source sections: {len(missing_source)}")
    print(f"- dead relative links: {len(dead_links)}")
    print(f"- topics missing in topic-index: {len(missing_topics_in_index)}")
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

    if missing_topics_in_index:
        print("## Topics Missing in topic-index")
        for name in missing_topics_in_index[:20]:
            print(f"- {name}")
        print()

    problems = any([short_pages, dup_titles, missing_source, dead_links, missing_topics_in_index])
    print(f"STATUS: {'WARN' if problems else 'OK'}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
