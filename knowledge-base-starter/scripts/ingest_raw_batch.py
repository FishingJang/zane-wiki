#!/usr/bin/env python3
from pathlib import Path
import argparse
import re
import shutil
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DST = ROOT / "raw" / "articles"

CUSTOM_SLUGS = {
    "Agentic Memory_ Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents": "agentic-memory-unified-long-and-short-term-memory-management",
    "阿里巴巴新论文：让LLM学会管理记忆，告别人工规则": "alibaba-llm-memory-management-without-manual-rules",
    "Hyperagents：AI学会如何自我改进": "hyperagents-ai-self-improvement",
    "12小时130万阅读，AI时代，产品不再护城河：公司形态才是": "ai-era-company-shape-not-product-moat",
    "企业 AI 转型的最大坑：给 Agent 装了最强大脑，却让它半失明": "enterprise-ai-agent-strong-brain-half-blind",
    "Agent开发之从 PRD 到架构总走样？这 4 个设计决策让 AI 不跑偏": "agent-development-prd-to-architecture-four-decisions",
    "一个文件让 AI Coding 效率翻倍：AGENTS.md 实践指南": "agents-md-practical-guide",
    "应该是全网最细最全的开发规范AGENTS.MD× CLAUDE.md × 团队实践方法【已开源】": "agents-md-claude-md-team-practices",
    "Harness Engineering：耗时一周，我是如何将应用的AI Coding率提升至90%的": "harness-engineering-ai-coding-90-percent",
    "Harness Engineering（驾驭工程）：2026年AI架构的终极命题": "harness-engineering-2026-ai-architecture",
    "Meta-Harness：让AI 改进自己的Harness": "meta-harness-ai-improves-harness",
    "Agent之Harness工程": "agent-harness-engineering",
    "「纯干货」几万字都讲不明白的Memory架构与思考": "memory-architecture-and-thinking",
    "SDD-RIPER 团队落地指南：如何让整个团队在一周内跑通大模型编程": "sdd-riper-team-rollout-guide",
    "别写 Markdown 了，用 HTML【译】": "stop-writing-markdown-use-html",
    "00_阅读摘要_AI工程化与Harness_AGENTS_2026-05-12": "reading-summary-ai-engineering-harness-agents",
}


def slugify(stem: str) -> str:
    if stem in CUSTOM_SLUGS:
        return CUSTOM_SLUGS[stem]
    text = unicodedata.normalize("NFKD", stem)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


def main():
    parser = argparse.ArgumentParser(description="Ingest markdown files into raw/articles with normalized naming.")
    parser.add_argument("src", help="Source directory containing markdown files")
    parser.add_argument("--date", required=True, help="Date prefix, e.g. 2026-05-13")
    parser.add_argument("--source", default="webclipper", help="Source label, e.g. webclipper")
    parser.add_argument("--dst", default=str(DEFAULT_DST), help="Destination directory")
    parser.add_argument("--copy", action="store_true", help="Actually copy files. Default is dry-run")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing targets")
    args = parser.parse_args()

    src = Path(args.src).expanduser().resolve()
    dst = Path(args.dst).expanduser().resolve()
    if not src.exists() or not src.is_dir():
        print(f"ERROR: source directory not found: {src}")
        sys.exit(2)

    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(src.glob("*.md"))
    if not files:
        print("ERROR: no markdown files found")
        sys.exit(2)

    existing_by_slug = {}
    for existing in dst.glob("*.md"):
        parts = existing.name.split("__", 2)
        if len(parts) == 3 and parts[1] == args.source:
            existing_by_slug[parts[2]] = existing.name

    print("# Raw Ingest Plan")
    print(f"- source dir: {src}")
    print(f"- target dir: {dst}")
    print(f"- date: {args.date}")
    print(f"- source label: {args.source}")
    print(f"- mode: {'copy' if args.copy else 'dry-run'}")
    print()

    planned = []
    skipped = 0
    for file in files:
        slug = slugify(file.stem)
        target = dst / f"{args.date}__{args.source}__{slug}.md"
        exists = target.exists()
        same_slug_other_date = existing_by_slug.get(target.name.split('__', 2)[2])
        action = "SKIP_EXISTS" if exists and not args.overwrite else "COPY"
        planned.append((file, target, action, same_slug_other_date))
        suffix = f" [existing variant: {same_slug_other_date}]" if same_slug_other_date and not exists else ""
        print(f"- {action}: {file.name} -> {target.name}{suffix}")

    if not args.copy:
        return

    for file, target, action, _same_slug_other_date in planned:
        if action == "SKIP_EXISTS":
            skipped += 1
            continue
        shutil.copy2(file, target)

    copied = len(planned) - skipped
    print()
    print("# Result")
    print(f"- copied: {copied}")
    print(f"- skipped_existing: {skipped}")


if __name__ == "__main__":
    main()
