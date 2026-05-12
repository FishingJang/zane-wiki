# Knowledge Base Starter

一个可复制的新知识库起步模板，支持两类常见入口：
- Markdown / WebClipper 型资料
- PDF / EPUB / 书籍型资料

目标不是只提供目录，而是把一个新知识库真正跑起来所需的三层底座一起交付：
1. `CLAUDE.md`：项目级规则
2. `prompts/*.md`：流程级入口
3. `scripts/*.py`：确定性执行入口

> 更新摘要（2026-05-12）
>
> 这版 starter 已从“目录骨架”升级为“可运行的最小知识库 runtime”：
> - 支持 `articles` / `books` 双入口
> - 支持 `raw -> notes -> wiki` 的书籍分支
> - 补齐 ingest report / health report / lint / health check 最小闭环
> - 引入 lifecycle 治理（`routed / seeded / parked / compiled`）
> - 引入 duplicate governance（重复来源、近似重复主题、同书重复副本等）
>
> 如果你是第一次进入这个仓库，建议阅读顺序：
> 1. `knowledge-base-starter/wiki/summaries/workflow-map.md`
> 2. `knowledge-base-starter/wiki/summaries/current-focus.md`
> 3. 再按资料类型运行对应 cycle

---

## 这套 starter 回顾总结自什么实践

这套模板不是凭空设计的，而是从两轮真实落地里收敛出来的：

### 第一轮：Markdown / WebClipper 型知识库
沉淀出的关键结论：
- 仅有 `raw/` 和 `wiki/` 还不够，必须补 `outputs/`、`prompts/`、`scripts/`
- 语义编译不能完全脚本化，脚本只负责确定性环节
- 需要最小健康检查、wiki lint 和报告生成，否则知识库会越跑越脏
- 索引、summary、overview 不能靠临时聊天维护，必须固化成文件

### 第二轮：PDF / EPUB / 书籍型知识库
补出的关键能力：
- 不能强行把 PDF / EPUB 走 markdown ingest 流程
- 必须拆成 `raw/books -> raw/notes -> wiki`
- 需要单独的书籍抽取 prompt
- 需要抽取脚本 `extract_books_to_notes.py`
- 需要在导航层引入 `cases/`、`investment-map.md` 这类第二阶段结构页

所以，这个 starter 现在默认已经是**双入口模板**，不是单一 markdown 模板。

---

## 适用场景

适合：
- 个人研究型知识库
- 产品 / 技术 / 商业 / 投资资料沉淀
- Obsidian + Agent 协作知识库
- 先用 Markdown Wiki 跑通，再决定是否引入更复杂检索层

不适合：
- 一开始就想做复杂数据库、RAG、向量库平台
- 还没确认知识结构就先做重系统设计

---

## 推荐目录结构

```text
knowledge-base/
├── raw/
│   ├── articles/      # markdown / webclipper 原始资料
│   ├── books/         # pdf / epub / 原件
│   └── notes/         # 从 books 抽取出的中间文本层
├── wiki/
│   ├── topics/
│   ├── concepts/
│   ├── cases/
│   ├── summaries/
│   └── indexes/
├── outputs/
│   └── reports/
├── prompts/
├── scripts/
├── README.md
└── CLAUDE.md
```

---

## 什么时候走哪条流程

### A. Markdown / WebClipper 资料
适用输入：网页文章、剪藏 markdown、纯文本笔记。

流程：
1. 原始 md 放临时目录
2. 运行 `scripts/run_ingest_cycle.py`
3. 把文件规范入库到 `raw/articles/`
4. 用 Agent 执行 `prompts/knowledge-base-ingest-and-compile.md`
5. 再跑检查 / 报告生成

### B. PDF / EPUB / 书籍资料
适用输入：PDF、EPUB、扫描件转文本后的资料。

流程：
1. 原件放入 `raw/books/`
2. 运行 `scripts/extract_books_to_notes.py`
3. 把可读文本沉到 `raw/notes/`
4. 用 Agent 执行 `prompts/book-ingest-and-extract.md`
5. 再把结构化内容编译进 `wiki/`

---

## 初始化方法

1. 复制本模板目录
2. 按你的项目名重命名根目录
3. 修改 `CLAUDE.md` 里的项目名、约束和目标
4. 如果是书籍型库，保留 `raw/books/`、`raw/notes/` 与 `prompts/book-ingest-and-extract.md`
5. 放入第一批资料
6. 按输入类型走对应流程
7. 运行健康检查与 lint
8. 如果走 markdown / webclipper 流程，可再用 `scripts/run_ingest_cycle.py`
9. 如果走 books 流程，不要调用 `run_ingest_cycle.py`，而是走：
   - `raw/books/`
   - `scripts/extract_books_to_notes.py`
   - `prompts/book-ingest-and-extract.md`

---

## 当前模板包含什么

### 项目级规则
- `CLAUDE.md`

### Prompt 层
- `prompts/knowledge-base-ingest-and-compile.md`
- `prompts/book-ingest-and-extract.md`

### 脚本层
- `scripts/ingest_raw_batch.py`
- `scripts/extract_books_to_notes.py`
- `scripts/kb_health_check.py`
- `scripts/wiki_lint.py`
- `scripts/generate_health_report.py`
- `scripts/run_ingest_cycle.py`

### 报告模板
- `outputs/reports/knowledge-base-health-check-template.md`

### 示例导航骨架
- `wiki/summaries/overview.md`
- `wiki/summaries/current-focus.md`
- `wiki/indexes/topic-index.md`
- `wiki/summaries/investment-map.md`

---

## 推荐的 wiki 生长顺序

如果是一个全新的知识库，优先按这个顺序生长：

1. 先建 1 个 topic 页
2. 再建 3~5 个核心 concept 页
3. 再补 summary / overview / index
4. 如果资料里有典型对象，再补 case 页
5. 第二轮再补估值、资本配置、方法边界这类第二层概念

这比一上来铺很多散页稳定得多。

---

## 最小验收标准

至少满足：
- raw 分层清楚
- wiki 有 topic / concept / summary / index 四层最小结构
- `python3 scripts/kb_health_check.py` 可执行
- `python3 scripts/wiki_lint.py` 可执行
- 导航页和索引页都存在
- 文件里没有 `1|` 这种工具展示污染
