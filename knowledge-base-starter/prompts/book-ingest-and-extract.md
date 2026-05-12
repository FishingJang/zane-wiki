# Book Ingest And Extract

适用于 PDF / EPUB / 书籍型资料。

## 目标
把书籍原件从 `raw/books/` 逐步推进到可进入 wiki 的结构化知识：
1. 原件入库
2. 文本抽取到 `raw/notes/`
3. 从 notes 提炼 topic / concept / case
4. 更新 summary / overview / index

## 执行原则
- 不要把 PDF / EPUB 直接当作 `raw/articles/*.md` 处理
- 优先使用 `raw/notes/` 作为语义编译输入层
- 先产出最小可用主题结构，再逐步补案例和方法页
- 书籍型知识库默认推荐的扩展顺序：
  - topic
  - core concepts
  - summary / index
  - cases
  - valuation / capital allocation concepts

## 最小输出要求
至少生成：
- 1 个 topic 页
- 3~5 个 concept 页
- 1 个 current-focus
- 1 个 overview
- 1 个 topic-index

## 检查要求
完成后至少运行：
```bash
python3 scripts/kb_health_check.py
python3 scripts/wiki_lint.py
```
