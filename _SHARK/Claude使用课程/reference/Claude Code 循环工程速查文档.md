---
title: Claude Code 循环工程速查文档
tags: [Claude Code, Loop, SKILL.md, /goal, /loop, /schedule, Proactive]
---

# Claude Code 循环工程速查文档（直接复制即用）

## 目录
1. 通用前置说明
2. Turn-based 回合制循环 SKILL.md
3. Goal-based 目标循环 /goal 完整指令 + 配套 SKILL.md
4. Time-based 定时循环 /loop /schedule 指令 + SKILL.md
5. Proactive 主动无人值守循环调度模板 + SKILL.md
6. 全局防死循环通用配置片段

---

## 通用前置说明
1. 所有 `SKILL.md` 放在项目根目录，Claude Code 自动加载；
2. 所有循环强制配置**最大迭代轮次**，防止 Token 无限消耗；
3. 验收标准必须**可量化、可自动校验**，禁止模糊描述；
4. 统一终止标记：`TASK_COMPLETED`，便于自动识别结束。

---

# 1. Turn-based 回合制循环（基础手动对话）SKILL.md

文件名：`SKILL.md`

```markdown
---
name: turn_based_self_check
description: 回合制对话每轮自动自检，减少人工反复确认
mode: turn-based
max_rounds_per_task: 8
stop_trigger: TASK_COMPLETED
---
# 自检执行流程（每轮对话自动执行）
1. 梳理当前已完成工作清单，对比用户原始需求
2. 自动执行项目校验脚本：lint、单元测试、构建打包
3. 收集报错、警告、功能缺失项逐条列出
4. 分两种分支判断：
   - 存在未解决问题：列出修复方案，等待用户确认后继续迭代
   - 全部需求满足、无报错：输出标记 TASK_COMPLETED，停止迭代

# 输出规范
- 未完成：【待修复】+ 问题清单 + 下一步修改方案
- 已完成：TASK_COMPLETED + 完整交付物汇总（代码/文档/接口）

# 约束规则
1. 单次迭代只解决一类问题，不并行大量修改
2. 上下文过长时自动精简历史无关日志
3. 不主动发起新任务，仅响应用户当前需求
```

**使用方式：** 无需特殊指令，正常发消息对话，Skill 自动生效。

---

# 2. Goal-based 目标导向循环

## 2.1 一键复制 /goal 启动指令模板

### 模板A：后端开发通用
```
/goal 开发用户管理模块REST接口
最大迭代轮次：12
验收标准：
1. 完整实现增删改查接口，入参出参参数校验齐全
2. 单元测试覆盖率 ≥ 85%，npm run test 无报错
3. 接口文档README.md 更新完整，包含请求示例
4. 无控制台Error、Lint零警告
全部达标输出：TASK_COMPLETED
```

### 模板B：前端页面开发通用
```
/goal 重构登录页UI与逻辑
最大迭代轮次：10
验收标准：
1. 还原设计稿样式，无布局错位、样式冲突
2. 表单校验、验证码、记住登录功能正常
3. 移动端自适应适配完成
4. 构建打包无警告，交互无卡顿
全部达标输出：TASK_COMPLETED
```

## 2.2 Goal 配套 SKILL.md

```markdown
---
name: goal_cycle_validator
description: /goal 目标循环专用自动化校验器
mode: goal-based
global_max_iter: 15
terminate_tag: TASK_COMPLETED
---
# 循环校验逻辑
1. 每轮修改完成后自动执行全量验收标准逐条核对
2. 统计未通过项数量，按优先级排序修复
3. 达到最大迭代轮次仍未达标，主动中止并输出阻塞问题清单
4. 全部标准满足，输出终止标记，停止循环

# 强制约束
1. 每次迭代只修复未通过项，不新增无关功能
2. 每轮结束输出【当前进度：X/全部验收项】
3. 连续3轮无进展直接终止循环，提示人工介入
```

---

# 3. Time-based 定时循环（/loop 本地轮询 /schedule 云端定时）

## 3.1 /loop 本地短时轮询指令模板（本地运行，关机失效）
```
/loop 每15分钟执行依赖漏洞扫描
最大单次循环轮次：5
验收标准：
1. 输出所有高危/中危依赖漏洞清单
2. 自动生成可执行升级修复脚本
3. 漏洞全部修复完成标记 TASK_COMPLETED
连续2轮无漏洞自动暂停循环
```

## 3.2 /schedule 云端长期定时指令模板（离线后台运行）
```
/schedule 每日08:00 自动检查代码PR并基础审查
单次任务最大迭代：8
停止条件：
1. 当日所有PR审查完毕输出 TASK_COMPLETED
2. 达到当日10次执行上限自动停止
任务内容：
1. 检查待合并PR代码规范
2. 自动运行单元测试
3. 生成审查反馈评论
```

## 3.3 Time-based 配套 SKILL.md

```markdown
---
name: time_cycle_scheduler
description: 定时循环统一校验与限流管控
mode: time-based
max_daily_runs: 10
max_single_iter: 8
terminate_tag: TASK_COMPLETED
---
# 定时执行规则
1. 每次定时触发先判断当日执行次数，到达上限直接跳过
2. 任务执行前清理上一轮冗余日志，控制上下文长度
3. 批量任务分段处理，单次最多处理5个子项
4. 无待处理任务时自动休眠，不占用Token

# 异常终止规则
1. 连续两轮执行报错，暂停定时并推送异常报告
2. 单次循环迭代耗尽上限，终止并留存未完成任务清单
```

---

# 4. Proactive 主动无人值守多Agent循环

## 4.1 调度启动指令模板
```
# 启动主动无人值守流水线
proactive pipeline: code_migration_auto_workflow
单任务最大迭代：10
全局每日执行上限：20
触发条件：检测到新分支/新工单自动唤醒
停止规则：
1. 单个迁移任务全部校验通过输出 TASK_COMPLETED
2. 当日执行达上限休眠至次日
3. 人工输入 STOP_PROACTIVE 强制关闭流水线
```

## 4.2 Proactive 专用 SKILL.md（生产级）

```markdown
---
name: proactive_pipeline_controller
description: 多Agent协同无人值守循环总控
mode: proactive
sub_agent_mode: goal-based
global_daily_quota: 20
single_task_max_iter: 10
terminate_tag: TASK_COMPLETED
emergency_stop: STOP_PROACTIVE
---
# 调度核心逻辑
1. 事件触发后自动分派子Agent执行Goal循环
2. 父Agent统一汇总所有子任务校验结果
3. 每日用量到达配额，暂停全部自动化任务
4. 任意子任务连续4轮无进展，冻结该工单等待人工

# 安全管控（必开）
1. 禁止自动合并高危代码、修改线上配置
2. 所有修改生成备份文件，保留回滚方案
3. 每次流水线执行输出Token消耗统计 /usage
4. 出现破坏性操作风险直接终止循环并告警
```

---

# 5. 全局通用防死循环片段（任意SKILL可追加）

粘贴在任意 `SKILL.md` 文件末尾即可生效：

```markdown
## 全局循环安全约束（通用）
1. 所有循环必须设置迭代硬上限，无上限禁止持续运行
2. 连续3轮修改后验收项无变化 → 判定死循环，立即终止
3. 上下文token超过120k自动压缩历史，仅保留需求+验收标准
4. 每轮循环末尾输出本轮消耗，超阈值自动降频
5. 人工输入 STOP_LOOP 可强制终止当前任意循环
```

---

# 使用快速提示

| 场景 | 用哪个 | 配套文件 |
|------|--------|---------|
| 简单临时改代码 | Turn-based | SKILL.md（自检） |
| 单项目复杂开发 | `/goal` | goal_cycle_validator |
| 每日巡检、定时扫描 | `/schedule` | time_cycle_scheduler |
| 企业自动化流水线 | Proactive | 整套模板 |
| 全部场景通用 | 追加 | 全局防死循环约束 |