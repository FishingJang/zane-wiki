# Knowledge Base Project Rules

## 项目性质
这是一个本地 Markdown 知识库项目。
目标是持续把 raw 资料编译为 wiki，并产出 outputs。

## 默认工作方式
- 默认直接执行增量更新，不先停在方案讨论
- 默认优先生成最小可用结果，而不是等待完整设计
- 默认围绕以下目录工作：
  - raw/
  - wiki/
  - outputs/
  - prompts/
  - scripts/
- 默认保留已有内容，在其基础上增量补充

## 输入类型边界
### 允许直接走 markdown ingest 的资料
- markdown 文件
- web clipper 导出的文章
- 纯文本笔记

这类资料应优先进入：
- `raw/articles/`

### 不要直接走 markdown ingest 的资料
- PDF
- EPUB
- 扫描件
- 图片型文档

这类资料应先走：
- 原件入 `raw/books/`
- 抽取文本入 `raw/notes/`
- 再由 Agent 基于 `raw/notes/` 编译到 `wiki/`

## 允许直接执行的事项
以下事项无需额外确认，直接执行：
- 新增或更新 wiki 主题页、概念页、案例页、索引页、summary 页
- 新增 outputs 下的报告、回答、幻灯片 markdown
- 基于 raw 资料做摘要、结构化整理、交叉链接
- 修复 wiki 内部链接、补来源、补索引
- 小范围重写单个 markdown 文件，只要目标明确且不删除大量信息
- 新建 `raw/books/`、`raw/notes/`、`wiki/cases/` 等低风险目录层

## 先做成，再优化
- 优先产出最小可用结果
- 不要为了结构偏好反复询问用户
- 不要因为“可能还有更优组织方式”而暂停执行
- 当前资料不足时，可以先产出骨架页并明确标注限制

## 默认决策规则
- 当存在多个合理输出结构时，不要先询问用户
- 默认选择最有助于知识库长期积累的结构
- 对于 wiki/ 下新增摘要页、索引页、概念页、案例页，如存在多个合理组织方式，默认先产出最小混合版，而不是提问
- 除非不同结构会导致信息删除、命名规范变化或目录重组，否则不要停下来确认

## 何时必须停下来确认
仅在以下情况需要确认：
- 要删除已有大量 wiki / outputs 内容
- 要改动目录结构或命名规范
- 要把当前单一来源结论上升为确定事实
- 要引入外部服务、数据库、向量库、RAG 或复杂新依赖
- 用户要求与当前规则明显冲突

## 输出要求
- 输出尽量为 Markdown
- 明确区分：事实 / 判断 / 不确定点
- 能引用来源就引用来源
- 结果优先落文件，不要只停留在聊天说明

## 导航层要求
- 新增 wiki 内容后，优先同步检查：
  - `wiki/indexes/topic-index.md`
  - `wiki/summaries/current-focus.md`
  - `wiki/summaries/overview.md`
- 当知识库进入第二阶段时，可补 `cases/`、`investment-map.md`、`topic-pipeline-board.md`、`material-promotion-rubric.md`、`duplicate-intake-policy.md`
- 当 scripts cycle 已开始运行时，应把 `outputs/reports/` 视为运行导航的一部分，而不只是附件目录
- 不要把所有流程文档和导航文档硬塞进 concepts 列表

## 生命周期判断要求
- 新材料默认先进入 `routed`，不要因为“看起来重要”就直接写 wiki
- 当材料开始显露主题价值时，可先写 seed 页，再决定是否扩为完整 topic
- OCR 弱、正文不足、只有元数据或杂讯的材料，默认优先判为 `parked`
- `parked` 不是失败，而是显式决策；如需重开，应先补 OCR / 清洗或等待形成主题簇
- 只有已进入稳定 wiki 结构、接入导航且通过检查的内容，才应视为 `compiled`

## 重复材料治理要求
- 重复处理同一目录后，先判断这次是重复来源、近似重复主题、同书重复副本，还是对旧材料的有效补充
- `--dupN` 只表示安全保留副本，不表示它已成为新增知识资产
- 对重复来源或近似重复主题，默认先写 ingest/report 判断，不要直接新增 topic / concept / summary
- 对同一本书再次进入，至少区分：重复副本、疑似新版候选、或可补强旧主题的补充来源
- 重复判断优先级高于继续编 wiki；先判断是否值得升级，再决定 raw / wiki 动作

## 风格要求
- 清晰、直接、克制
- 先给结果，再给解释
- 不要空泛，不要过度设计
