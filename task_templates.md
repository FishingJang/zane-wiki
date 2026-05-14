## 这个是常用任务模板列表

- 你可以直接复制的任务模板

模板 1：把 raw 编译成 wiki
claude -p "

目标：将 raw/ 中新增资料编译进 wiki/

约束：不要删除已有 wiki 页面；优先增量更新；保留来源引用

完成标准：

1. 识别新增主题与概念

2. 更新对应 wiki 页面

3. 建立必要链接

4. 输出修改摘要

" --allowedTools "Read,Edit,Write,Bash" --max-turns 12


模板 2：围绕 wiki 做专题总结
claude -p "

目标：基于 wiki/ 和 raw/ 输出一个专题总结

约束：只基于现有材料；不编造来源

完成标准：

1. 生成一篇结构化 markdown 报告

2. 标出关键结论

3. 标出不确定点

4. 保存到 outputs/reports/

" --allowedTools "Read,Edit,Write" --max-turns 10


模板 3：做知识库健康检查
claude -p "

目标：对 wiki/ 做健康检查

完成标准：

1. 找出重复概念页

2. 找出断链或弱链接

3. 找出缺少来源引用的页面

4. 找出值得新增的主题页

5. 输出检查报告到 outputs/reports/

" --allowedTools "Read,Edit,Write,Bash" --max-turns 10


模板 4：生成汇报材料
claude -p "

目标：基于 wiki/ 生成一份汇报材料

约束：内容面向业务或技术决策者；避免过度学术化

完成标准：

1. 生成 Marp markdown

2. 控制在 10 页以内

3. 包含问题、判断、结论、建议

4. 输出到 outputs/slides/

" --allowedTools "Read,Edit,Write" --max-turns 10
