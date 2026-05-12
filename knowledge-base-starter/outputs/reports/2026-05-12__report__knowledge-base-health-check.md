# Knowledge Base Health Check Report

- 日期：2026-05-12
- 范围：全库完整检查
- 执行者：Agent
- 证据等级：L1
- 总状态：**OK**

## 一、检查范围

- raw 范围：`raw/`
- wiki 范围：`wiki/`
- outputs 范围：`outputs/reports/`

## 二、脚本结果：kb_health_check.py

```text
# Knowledge Base Health Check

## Counts
- raw articles: 0
- raw books: 0
- raw notes: 0
- topics: 0
- concepts: 0
- cases: 0
- indexes: 1
- summaries: 3

## Navigation Presence
- topic-index exists: True
- current-focus exists: True
- overview exists: True
- investment-map exists: True
- books layer exists: False
- notes layer exists: False

## Minimal Link Checks
- topic-index references summary layer: True
- overview references topic-index: True

## Hygiene
- line-number-pollution hits: 0

STATUS: OK
```

## 三、脚本结果：wiki_lint.py

```text
# Wiki Lint Report

## Summary
- total wiki pages: 4
- short pages: 0
- duplicate titles: 0
- missing source sections: 0
- dead relative links: 0
- topics missing in topic-index: 0

STATUS: OK
```

## 四、判断

### 可确认判断
- 当前健康检查脚本已可运行
- 当前 wiki lint 脚本已可运行
- 本次报告直接基于本地仓库实时脚本输出生成

### 风险点
- 当前检查仍偏“最小可用”，尚未覆盖更复杂的概念重复检测与语义级合并建议
- `run_ingest_cycle.py` 默认只覆盖 markdown / webclipper 入库分支；书籍型资料应走 `raw/books -> raw/notes -> prompts/book-ingest-and-extract.md` 这条链路

### 不确定点
- 当后续规模继续扩张时，现有 topic-index 是否会继续膨胀，仍需下一轮实战验证
- 当 books / notes 规模提升后，是否需要单独的 notes 质量检查脚本，仍需视资料复杂度决定

## 五、建议动作

1. 继续补一键编排入口，把 raw 入库、agent 编译、检查报告串起来
2. 后续视规模补 source-index / workflow-index
3. 未来再补更强的重复概念与弱链接检测

## 六、涉及文件

- `scripts/kb_health_check.py`
- `scripts/wiki_lint.py`
- `scripts/generate_health_report.py`
- `outputs/reports/2026-05-12__report__knowledge-base-health-check.md`
