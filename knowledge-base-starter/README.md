# Knowledge Base Starter

一个可复制的新知识库起步模板，支持两类常见入口：
- Markdown / WebClipper 型资料
- PDF / EPUB / 书籍型资料

目标不是只提供目录，而是把一个新知识库真正跑起来所需的三层底座一起交付：
1. `CLAUDE.md`：项目级规则
2. `prompts/*.md`：流程级入口
3. `scripts/*.py`：确定性执行入口

---

## 这套 starter 回顾总结自什么实践

这套模板不是凭空设计的，而是从多轮真实落地里收敛出来的：

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

### 第三轮：混合目录与知识生命周期治理
新增的关键结论：
- 混合目录首先是**路由问题**，不是摘要问题
- 需要把材料状态从“文件已存在”升级为“生命周期已判断”
- `raw` 可以混合，但 `wiki` 不能一锅炖
- 不是所有 routed 材料都值得升 seed，更不是所有 seed 都该立刻 compiled
- 需要把判断规则写进库内，而不是每次靠聊天重做决策

### 第四轮：重复材料治理
新增的关键结论：
- 重复处理同一目录后，缺口往往不在 routing，而在 duplicate governance
- `--dupN` 只是安全落库策略，不等于新知识资产
- 近似重复 article 不该自动生成新的 topic / concept
- 同一本书再次进入时，要区分重复副本、新版本候选、还是仅需在 report 记录
- 重复判断应先落 report，再决定 raw / wiki 的后续动作

所以，这个 starter 现在默认已经是：
1. **双入口模板**（articles/books）
2. **分层模板**（raw/wiki/outputs）
3. **带最小生命周期治理的模板**（routed/seeded/parked/compiled）
4. **带最小重复材料治理的模板**（duplicate-source / near-duplicate-topic / book-duplicate-copy / supplemental-source）

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

## 什么资料该走哪条流程

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
2. 运行 `scripts/run_books_cycle.py`
3. 自动调用 `scripts/extract_books_to_notes.py`，把可读文本沉到 `raw/notes/`
4. 用 Agent 执行 `prompts/book-ingest-and-extract.md`
5. 再把结构化内容编译进 `wiki/`

### C. 混合目录
适用输入：一个目录里同时含有 `.md / .html / .pdf / .epub`。

处理原则：
1. 先识别和分流，不要一锅总结
2. 忽略 HTML sidecar 资源目录（如 `*_files/`）
3. `.md / .html` → `raw/articles/`
4. `.pdf / .epub` 原件 → `raw/books/`
5. 书籍抽取文本 → `raw/notes/`
6. 写一份 ingest report，记录每个文件走向
7. 如果发现重复来源或近似重复材料，先按 `wiki/summaries/duplicate-intake-policy.md` 做重复判断，再决定是否继续升级

---

## 初始化方法

1. 复制本模板目录
2. 按你的项目名重命名根目录
3. 修改 `CLAUDE.md` 里的项目名、约束和目标
4. 如是书籍型或混合型知识库，保留 `raw/books/`、`raw/notes/` 与书籍相关 prompt/script
5. 放入第一批资料
6. 先按输入类型完成路由
7. 再决定哪些材料进入 wiki
8. 跑健康检查与 lint

---

## 当前模板包含什么

### 项目级规则
- `CLAUDE.md`

### Prompt 层
- `prompts/knowledge-base-ingest-and-compile.md`
- `prompts/book-ingest-and-extract.md`

### 脚本层
- `scripts/ingest_raw_batch.py`
- `scripts/generate_ingest_report.py`
- `scripts/extract_books_to_notes.py`
- `scripts/kb_health_check.py`
- `scripts/wiki_lint.py`
- `scripts/generate_health_report.py`
- `scripts/run_ingest_cycle.py`
- `scripts/run_books_cycle.py`

### 报告模板
- `outputs/reports/knowledge-base-ingest-report-template.md`
- `outputs/reports/knowledge-base-health-check-template.md`

### 阶段性说明 / Release Notes
- `outputs/reports/2026-05-12__template-release__dual-ingest-knowledge-base-starter-v1.md`

### 示例导航骨架
- `wiki/summaries/overview.md`
- `wiki/summaries/current-focus.md`
- `wiki/summaries/workflow-map.md`
- `wiki/summaries/topic-pipeline-board.md`
- `wiki/summaries/material-promotion-rubric.md`
- `wiki/summaries/duplicate-intake-policy.md`
- `wiki/indexes/topic-index.md`
- `wiki/summaries/investment-map.md`

---

## 推荐的 wiki 生长顺序

如果是一个全新的知识库，优先按这个顺序生长：

### 第一阶段：先跑通基础结构
1. 先完成第一批原料入库
2. 建 1 个 topic 页
3. 建 3~5 个核心 concept 页
4. 补 summary / overview / index

### 第二阶段：补导航与案例
5. 如资料里有典型对象，再补 case 页
6. 补 `topic-pipeline-board.md`，开始显式区分 active / incubating / parked
7. 补 `material-promotion-rubric.md`，把升级规则写进库里

### 第三阶段：再补第二层概念
8. 再补估值、资本配置、方法边界、人物流派这类第二层页面

这比一上来铺很多散页稳定得多。

---

## 材料生命周期最小模型

starter 默认建议用这 6 个状态词：
- `inbox`
- `routed`
- `seeded`
- `compiled`
- `parked`
- `archived`

最小落地要求不是元数据系统，而是：
- 至少有一页 `topic-pipeline-board.md` 作为状态面板
- 至少有一页 `material-promotion-rubric.md` 作为判断清单
- 当开始出现重复来源、近似重复 article 或同书重复副本时，补一页 `duplicate-intake-policy.md` 作为重复治理规则

这样未来处理新材料时，不必每次重开“这东西值不值得编 wiki”和“这次算不算新材料”的讨论。

---

## 最小验收标准

至少满足：
- raw 分层清楚
- wiki 有 topic / concept / summary / index 四层最小结构
- 存在 `workflow-map.md`
- 存在 `topic-pipeline-board.md`
- 存在 `material-promotion-rubric.md`
- 在出现重复入库场景后，存在 `duplicate-intake-policy.md`
- `python3 scripts/kb_health_check.py` 可执行
- `python3 scripts/wiki_lint.py` 可执行
- 导航页和索引页都存在
- 文件里没有 `1|` 这种工具展示污染
