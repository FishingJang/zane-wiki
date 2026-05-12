# Knowledge Base Ingest and Compile Prompt

适用于任意具备本地文件读写能力的 Agent，而不绑定 Claude Code。

## 目标

把一批新进入临时目录的 Markdown 资料，按知识库规则完成：
1. 规范入库到 `raw/articles/`
2. 基于新增 raw 资料增量编译 `wiki/`
3. 更新索引、当前摘要和入口页
4. 做最小卫生检查
5. 输出本轮结果摘要

## 项目背景

这是一个本地 Markdown 知识库项目。
目标不是先上复杂 RAG，而是先稳定跑通：
- raw -> wiki -> outputs
- 可重复
- 可审查
- 可维护

## 目录分层

- `raw/`：原始资料层，尽量保真
- `wiki/`：结构化知识层，不直接堆原文
- `outputs/`：任务交付层
- `prompts/`：可复用执行提示
- `scripts/`：确定性检查与辅助脚本

## 执行规则

### 1. raw 入库规则
- 网页/文章 markdown 默认进入 `raw/articles/`
- 文件命名统一为：`日期__来源__主题.md`
- 原文尽量保真，不在 raw 层过度改写

### 2. wiki 编译规则
围绕本批新增 raw，优先产出：
- topic 页
- concept 页
- index 页
- current-focus / overview 更新

要求：
- 不直接复制 raw 原文进入 wiki
- wiki 页面必须是结构化整理结果
- 优先形成“topic + concept + index + summary”的最小知识网络

### 3. 页面组织规则
- topic：一组资料共同支撑的主题层
- concept：较稳定、可复用的概念层
- summaries：本轮摘要、overview、SOP 等导航资产
- indexes：导航入口，不要让概念列表和流程文档混在一起无区分

### 4. 导航更新规则
新增或修改 wiki 页面后，至少同步更新：
- `wiki/indexes/topic-index.md`
- `wiki/summaries/current-focus.md`
- 如有必要，更新 `wiki/summaries/overview.md`

### 5. 卫生检查规则
必须检查：
- 行号污染（如 `1|`、`2|`）
- 重复段落或重复 bullet
- 新页面是否进入索引
- 基本计数是否同步

如果怀疑页面已污染：
- 不要在脏页上持续 patch
- 直接整页重写
- 重写后重新读取验证

## 输出要求

完成后请：
1. 直接落文件，不只在聊天里描述
2. 给出本轮新增 / 修改文件列表
3. 说明本轮新增主题与概念
4. 说明是否通过卫生检查
5. 给出下一步建议
