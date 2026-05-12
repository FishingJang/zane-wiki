#!/usr/bin/env python3
from pathlib import Path
import argparse
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ROOT / "raw" / "books"
NOTES = ROOT / "raw" / "notes"


def slugify(name: str) -> str:
    text = name.lower()
    text = re.sub(r"\.(pdf|epub)$", "", text)
    text = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


def extract_pdf(src: Path) -> str:
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        result = subprocess.run(['pdftotext', str(src), str(tmp_path)], text=True, capture_output=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or 'pdftotext failed')
        return tmp_path.read_text(encoding='utf-8', errors='ignore')
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def strip_html(text: str) -> str:
    text = re.sub(r'<script.*?>.*?</script>', ' ', text, flags=re.S | re.I)
    text = re.sub(r'<style.*?>.*?</style>', ' ', text, flags=re.S | re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_epub(src: Path) -> str:
    chunks = []
    with zipfile.ZipFile(src, 'r') as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(('.html', '.xhtml', '.htm'))]
        for name in names:
            try:
                data = zf.read(name).decode('utf-8', errors='ignore')
            except Exception:
                continue
            cleaned = strip_html(data)
            if cleaned.strip():
                chunks.append(cleaned)
    return '\n\n'.join(chunks)


def summarize_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    preview = '\n'.join(lines[:80])
    return preview[:12000]


def build_note(src: Path, extracted: str, quality: str) -> str:
    summary = summarize_text(extracted)
    return f'''# {src.stem}

## Source File
- `raw/books/{src.name}`

## Extraction Status
- quality: {quality}
- extracted_chars: {len(extracted)}

## Notes
- 这是自动抽取的原始可读文本预处理结果
- 仅用于后续摘要、主题提炼与 wiki 编译前的中间层
- 若排版错乱、章节顺序异常或噪声较多，需要后续人工/Agent 再整理

## Extracted Preview

```text
{summary}
```
'''


def main():
    parser = argparse.ArgumentParser(description='Extract PDF/EPUB books into raw/notes markdown previews.')
    parser.add_argument('--src-dir', default=str(BOOKS), help='Directory containing raw book files')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of files processed (0 = all)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing notes')
    args = parser.parse_args()

    src_dir = Path(args.src_dir).expanduser().resolve()
    NOTES.mkdir(parents=True, exist_ok=True)
    files = sorted([p for p in src_dir.iterdir() if p.is_file() and p.suffix.lower() in {'.pdf', '.epub'}])
    if args.limit > 0:
        files = files[:args.limit]

    if not files:
        print('ERROR: no PDF/EPUB files found')
        sys.exit(2)

    for src in files:
        stem = slugify(src.name)
        out = NOTES / f'extracted__{stem}.md'
        if out.exists() and not args.overwrite:
            print(f'SKIP_EXISTS {out.name}')
            continue
        if src.suffix.lower() == '.pdf':
            extracted = extract_pdf(src)
            quality = 'raw-pdftotext'
        else:
            extracted = extract_epub(src)
            quality = 'raw-epub-html-strip'
        out.write_text(build_note(src, extracted, quality), encoding='utf-8')
        print(f'WROTE {out.name} chars={len(extracted)} quality={quality}')


if __name__ == '__main__':
    main()
