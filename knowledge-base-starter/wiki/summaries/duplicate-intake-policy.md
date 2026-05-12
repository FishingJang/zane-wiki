# Duplicate Intake Policy

## 目的
这页回答一个在真实重复入库场景里迟早会出现的问题：

**同一批目录被重复处理、同主题近似文章再次进入、同一本书再次进入时，知识库应该怎么接，而不是无脑继续生成新资产？**

它处理的不是“技术去重算法”，而是**重复材料治理规则**。

默认目标只有三个：
1. 不覆盖旧原件
2. 不把重复来源误当成新增知识资产
3. 让 report、raw、wiki 三层对“这次到底算新增、重复、还是新版本”说同一种话

## 先讲结论
- **重复治理优先级高于继续编 wiki**
- 再次看到近似材料时，先判断它属于哪一种重复，再决定是否落 raw、是否只记 report、是否升级 wiki
- `raw` 可以保守保留副本，但 `wiki` 不应该因为重复来源而膨胀

## 重复材料的四种常见类型

### 1. 完全重复来源
特征：
- 标题、正文主体、来源、版本都基本一致
- 只是重复抓取、重复复制、再次处理同一目录

默认动作：
- **允许保守落 raw，但不视为新增知识资产**
- report 中明确记为 `duplicate-source`
- 不新建 topic / concept / summary
- 如果已有同名原件，为了安全可保留 `--dupN`，但语义上仍视为“重复来源”

### 2. 同主题近似文章
特征：
- 不是逐字相同
- 但主题、核心论点、结论结构高度重合
- 常见于同一内容被平台改写、转载、压缩、换标题重发

默认动作：
- 可以入 `raw/articles/`，但先标记为 `near-duplicate-topic`
- 优先更新已有 topic / concept 的来源视角，而不是新开一条 wiki 线
- 如果新增信息很弱，只记 report，不推进 wiki

### 3. 同一本书的新旧版本或重复副本
特征：
- 书名基本一致
- 可能只是不同来源站、不同文件格式、不同清晰度
- 也可能是真正的新版本/新版次

默认动作：
- 不覆盖旧文件
- 原件可用 `--dupN` 保留，保证可追溯
- report 中必须进一步区分：
  - `book-duplicate-copy`：同书重复副本，信息价值没有明显新增
  - `book-new-edition-candidate`：疑似新版或更高质量版本，值得后续比对
- 如果只是重复副本，默认**不新增 seed / compiled 动作**
- 如果明显是更高质量版本，默认先进入 `routed`，等待重新评估，不要直接覆盖旧 notes/wiki

### 4. 旧材料的新补充
特征：
- 同主题或同对象
- 但提供了明显新增的章节、案例、数据、方法或反例
- 它虽然重复相关，但不是纯重复

默认动作：
- 视为 `supplemental-source`
- 可以进入 raw
- 如果它明显补强现有 wiki，优先增补已有页面，而不是再造一页平行资产

## 默认判断顺序
1. **先判断是不是重复来源，不要先问要不要编 wiki**
2. 判断属于：`duplicate-source / near-duplicate-topic / book-duplicate-copy / book-new-edition-candidate / supplemental-source`
3. 再决定动作：
   - 只记 report
   - 落 raw 但不升格
   - 落 raw 并等待重评
   - 更新现有 wiki
4. 最后才考虑是否需要新增 wiki 页面

## raw / report / wiki 三层各自怎么做

### raw 层
原则：
- raw 首先负责**不丢材料**，不是负责“自动证明它值得升级”
- 所以重复材料可以保守保留，但要让命名和 report 说明它是重复，而不是新增资产

默认建议：
- article 近似重复：可以保留 raw，但不要因此推导出新的 wiki 义务
- book 重复副本：允许 `--dupN`
- 真正可疑的新版本：保留文件，等待对比后再决定是否替代旧版本

### report 层
report 是重复治理的主记录层。

每次 ingest 遇到重复时，至少要记清：
- 本次文件名
- 命中的既有文件或既有主题
- 重复类型
- 本次动作
- 是否需要后续人工/Agent 重评

一句话原则：
**重复判断先落 report，再决定是否落 wiki。**

### wiki 层
默认约束：
- 重复来源本身不是新 wiki 资产
- 近似主题不是自动新 topic
- 新版本候选不是自动重写旧页面

优先动作顺序：
1. 不动 wiki
2. 给已有页补来源
3. 更新 seed / topic 页中的“材料簇判断”
4. 只有当它带来明显新增结构时，才考虑新页

## 什么时候只记 report，不值得继续动作
满足大部分以下信号时，默认只记 report：
- 与已有 raw 基本同文
- 只是来源站或文件名不同
- 主题完全已被已有 wiki 吸收
- 没有新增正文支撑、案例、数据或反例
- 再编一次只会制造重复 topic / concept

## 什么时候虽然重复相关，但值得继续保留
满足以下任一条件，可保留并等待后续判断：
- 文件质量明显更高（OCR 更完整、排版更干净、章节更全）
- 虽同主题，但新增了关键方法、案例或边界条件
- 现有 wiki 只做了 seed，它能支持后续扩编
- 它可以作为反例、比较对象或版本差异样本

## 和生命周期状态怎么衔接
重复治理不是替代 lifecycle，而是它前面的一层判断。

建议顺序：
1. 先做 duplicate intake judgment
2. 再决定它进入哪个 lifecycle 状态

常见映射：
- `duplicate-source` → 通常只记 report，或保守留 raw，但不升 `seeded`
- `near-duplicate-topic` → 多数停在 `routed`
- `book-duplicate-copy` → 多数停在 `routed` 或只记 report
- `book-new-edition-candidate` → 先 `routed`，待重评
- `supplemental-source` → 可进入 `routed`，必要时支持已有 `seeded/compiled` 页面增补

## 最小工作准则
1. 不因为重复来源扩张 wiki
2. 不因为怕丢材料而覆盖旧文件
3. `--dupN` 是安全策略，不等于它值得升级
4. 重复判断先写进 report，再决定后续动作
5. 真正的新信息优先并入已有知识资产，而不是平行再造一份

## 相关页面
- [[workflow-map.md]]
- [[topic-pipeline-board.md]]
- [[material-promotion-rubric.md]]
- [[../indexes/topic-index.md]]

## 配套报告模板
- `outputs/reports/knowledge-base-ingest-report-template.md`
- `outputs/reports/knowledge-base-health-check-template.md`
