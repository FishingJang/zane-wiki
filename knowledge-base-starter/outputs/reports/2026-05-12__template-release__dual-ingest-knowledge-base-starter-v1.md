# Template Release Note — Dual Ingest + Lifecycle + Duplicate Governance

- 日期：2026-05-12
- 范围：`templates/knowledge-base-starter`
- 性质：阶段性收口说明

## 这次升级解决了什么
这套 starter 现在不再只是一个“目录模板”，而是一个**能工作的知识库 starter**。

它已经从最初的 markdown/wiki 起步骨架，升级成支持以下三层能力的版本：
1. **双入口**：articles / books
2. **最小治理**：lifecycle / duplicate governance
3. **最小运行闭环**：ingest report / health report / lint / health check

## 当前已具备的能力

### 1. 双入口运行
- Markdown / WebClipper 资料可走 `scripts/run_ingest_cycle.py`
- PDF / EPUB / 书籍资料可走 `scripts/run_books_cycle.py`
- books 分支默认走 `raw/books -> raw/notes -> wiki`

### 2. 最小生命周期治理
已具备：
- `topic-pipeline-board.md`
- `material-promotion-rubric.md`

可以显式表达：
- `routed`
- `seeded`
- `parked`
- `compiled`

### 3. 重复材料治理
已具备：
- `duplicate-intake-policy.md`
- ingest report 模板中的重复判断字段
- health report 对重复治理是否落地的联动检查

当前支持的重复治理语义包括：
- `duplicate-source`
- `near-duplicate-topic`
- `book-duplicate-copy`
- `book-new-edition-candidate`
- `supplemental-source`

### 4. report / health 最小闭环
articles 分支现在可自动产出：
- raw ingest
- ingest report
- health report

books 分支现在可自动产出：
- extract to notes
- ingest report
- health report

### 5. books 提取失败时不再整条链路崩掉
当前策略是：
- PDF 提取失败时，仍写出 `raw/notes/extracted__*.md`
- 并标记 `quality: pdf-extract-failed`
- 让它进入 report / parked 候选，而不是直接把整个 cycle 弄死

## 当前明确保留的自动化边界
这套 starter 现在是**半自动知识库 runtime**，不是全自动知识工厂。

### 脚本已负责
- 文件路由
- 书籍文本抽取
- 最小 ingest report
- 最小 health report
- kb health check
- wiki lint
- 弱失败信号显式化

### Agent 仍负责
- 主题提炼
- 概念归并
- case 抽取
- 交叉链接
- wiki 结构化编译
- 重复语义判断补全
- 生命周期最终判断

## 当前还没有自动化的部分
以下不是缺陷，而是有意保留的语义边界：
- 近似重复文章自动识别
- 书籍新旧版本自动判别
- wiki 全自动语义编译
- notes 质量强评分
- report 与 wiki topic/index 的自动联动更新

## 对使用者意味着什么
如果你复制这套 starter，新项目现在至少可以直接得到：
- 一套明确的双入口知识库流程
- 一套最小可运行的 scripts 层
- 一套最小治理文档
- 一套最小报告闭环

你不再需要从 README 和脚本里自己猜流程，也不需要每次重新争论：
- PDF 能不能直接走 markdown ingest
- 重复来源算不算新知识资产
- 弱 OCR 资料要不要硬编 wiki

## 推荐使用顺序
1. 先看 `wiki/summaries/workflow-map.md`
2. 再看 `wiki/summaries/current-focus.md`
3. 然后按资料类型跑对应 cycle
4. 再用 Agent 补 semantic compile
5. 最后用 `topic-pipeline-board.md` / `material-promotion-rubric.md` / `duplicate-intake-policy.md` 做治理判断

## 本次阶段性交付结论
这轮 starter 升级已经达到一个清晰的阶段性状态：

**它已经不是“需要你自己补全运行逻辑的模板”，而是“带最小运行闭环和治理边界的 starter”。**

下一阶段如果要继续升级，优先级应是：
1. 真实 repeated-ingest 批次下的 duplicate judgment 自动化增强
2. books 质量信号更细化
3. report 与 wiki 导航层的更强联动
