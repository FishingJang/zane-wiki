# Current Focus

## 当前主线
这是一个刚初始化的知识库。当前应先完成：
1. 先读 [[workflow-map.md]]，判断资料该走哪条入口
2. 第一批资料完成路由，进入 `raw/articles/` 或 `raw/books -> raw/notes/`
3. 形成 1 个 topic
4. 形成 3~5 个核心 concept
5. 补齐 overview / index
6. 如开始出现混合资料批次，补 `topic-pipeline-board.md` 与 `material-promotion-rubric.md`
7. 如开始重复处理同一目录或反复抓到同主题资料，补 `duplicate-intake-policy.md`
8. 如已跑过 cycle，先看 `outputs/reports/*.md`，再决定下一步要补 wiki、补治理，还是补提取质量

## 当前判断
不要一开始就把知识库做复杂。
先形成一个可读、可维护、可继续增量扩展的最小结构。

当知识库开始接收混合材料时，优先遵守：
- 先路由，再判断
- raw 可以混合，wiki 不要一锅炖
- 不是所有 routed 材料都值得升 seed
- OCR 弱材料可以直接 parked，不必硬编 wiki

当知识库开始接收重复材料时，优先遵守：
- 先判断这次算不算新材料，再决定是否继续升级
- `--dupN` 只代表安全保留，不代表新增知识资产
- 近似重复主题优先并回已有页面，而不是平行再造一页

当知识库已经开始跑 scripts cycle 时，优先遵守：
- ingest report / health report 已自动产出，不代表 wiki 已自动完成
- `STATUS: OK` 只说明结构健康，不说明语义编译已完成
- books 分支若出现 `quality: pdf-extract-failed` 或极低 `extracted_chars`，默认先按 weak signal 处理，再决定是否重做 OCR

## 当前建议
第二阶段默认补这三页：
- [[topic-pipeline-board.md]]
- [[material-promotion-rubric.md]]
- [[duplicate-intake-policy.md]]

如已进入运行阶段，再配合查看：
- `outputs/reports/knowledge-base-ingest-report-template.md`
- `outputs/reports/knowledge-base-health-check-template.md`
- `outputs/reports/2026-05-12__template-release__dual-ingest-knowledge-base-starter-v1.md`

这样后续处理新材料时，就不必每次重开状态判断、重复治理和运行边界讨论。
