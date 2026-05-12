# Knowledge Base Ingest Report Template

- 日期：YYYY-MM-DD
- 批次：wave1 / wave2 / mixed-ingest / books-cycle / custom
- 来源目录：
- 执行者：Agent / Human
- 处理模式：articles-only / books-only / mixed
- 是否启用重复判断：yes / no

## 一、本轮输入概览
- 输入文件总数：
- `.md / .html` 数量：
- `.pdf / .epub` 数量：
- 忽略资源文件 / sidecar 数量：

## 二、路由结果
### 1. Articles 路径
- 新增到 `raw/articles/`：
- 因重复判断未继续升格：
- 备注：

### 2. Books 路径
- 新增到 `raw/books/`：
- 新增到 `raw/notes/`：
- 提取失败 / 待补 OCR：
- 备注：

### 3. 本轮未处理项
- 

## 三、重复判断总览
- `duplicate-source`：
- `near-duplicate-topic`：
- `book-duplicate-copy`：
- `book-new-edition-candidate`：
- `supplemental-source`：
- 无重复命中：

## 四、重复判断明细
> 没有命中时可写“本轮无”。

| 本次文件 | 命中对象 | 重复类型 | 本次动作 | 是否待重评 | 备注 |
| --- | --- | --- | --- | --- | --- |
|  |  | `duplicate-source / near-duplicate-topic / book-duplicate-copy / book-new-edition-candidate / supplemental-source` | `report-only / keep-raw / keep-raw-and-hold / merge-into-existing-wiki` | yes / no |  |

## 五、生命周期判断
- 新进入 `routed`：
- 新进入 `seeded`：
- 保持 `parked`：
- 新进入 `compiled`：

## 六、可确认判断
- 

## 七、风险点
- 

## 八、不确定点
- 

## 九、建议动作
1. 
2. 
3. 

## 十、涉及文件
- 

## 附：最小填写规则
- 只要本轮有 ingest，就至少写清“来源目录、路由结果、涉及文件”。
- 只要本轮出现重复来源或近似重复材料，就必须填写“重复判断总览”和“重复判断明细”。
- `--dupN` 只表示安全保留，不表示这是新增知识资产。
- 如果重复材料没有新增信息，优先写 `report-only`，不要自动新增 wiki 页面。
- 如果是旧材料的有效补充，优先写 `merge-into-existing-wiki`，而不是平行新建一页。
