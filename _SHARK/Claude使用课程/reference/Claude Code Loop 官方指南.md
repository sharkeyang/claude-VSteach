---
title: Claude Code Loop 四层模型
source: Feisky 公众号
date: 2026-07-01
url: https://mp.weixin.qq.com/s/DVjVwFs7EPIr9F-39-BKQw
tags: [Claude Code, Loop, Agent, /goal, /loop, /schedule]
---

# Claude Code Loop 四层模型解析

> 原文：Feisky 公众号转述 Claude Code 官方博客
> 核心问题：Loop 用不好，往往不是模型不行，是你选错了层级

## 核心框架

Loop 分四层，区分标准是**你愿意交出去什么**：

| 层级 | 你交出去的 | 适合场景 | 用什么工具 |
|------|-----------|---------|-----------|
| **Layer 1: Turn-based** | 验证步骤 | 探索性任务、一次性修改 | Skill |
| **Layer 2: Goal-based** | 停止条件 | 有明确完成标准的任务 | `/goal` |
| **Layer 3: Time-based** | 触发时机 | 周期性工作、监控外部系统 | `/loop`、`/schedule` |
| **Layer 4: Proactive** | 整个决策流程 | 长期运行的定型工作流 | 以上全部 + 动态工作流 |

**递进关系**：你交出去的东西越多，Claude Code 自动完成的任务也就越多，但成本也越高。

---

## 第一层：Turn-based — 交出验证步骤

这是最基础的模式。你发 prompt → Claude Code 读代码/改代码/跑测试/返回结果 → 等你的下一条指令。

**提效方法**：把你的验证步骤写成 Skill。例如前端改按钮后：

```markdown
---
name: verify-frontend-change
---

1. 启动 dev server，在浏览器中打开改动页面。
2. 直接与改动交互（点按钮、填表单），确认预期行为。
3. 检查浏览器 console：不能有新的 error 或 warning。
4. 用 Chrome Devtools MCP 跑一次性能追踪。
```

这一层交出去的是"怎么确认做对了"。做什么、做到什么程度，还是你说了算。

---

## 第二层：Goal-based — 交出停止条件

Turn-based 的问题是复杂任务一轮搞不定，Claude Code 频繁停下来问你要决策。`/goal` 解决这个问题。

```bash
/goal 把首页 Lighthouse 分数提到 90 以上，最多试 5 次。
```

**关键要点**：
- 停止条件必须是**确定性**的（数字、测试通过数、分数阈值）
- 描述性结果需要大模型自评，很不靠谱
- Lighthouse 92 分这种确定性结果它才能判断得准
- 独立评估模型检查条件，不满足就打回去继续

**完成契约**：把"做完"从主观判断变成可验证的合约，agent 才能真正闭环。

---

## 第三层：Time-based — 交出触发时机

前两种都是手动触发。有些工作是周期性的，比如每天早上总结 Slack 消息，或者持续盯着 PR 等 review。

```bash
/loop 5m 检查我的 PR，处理 review 评论，修复挂掉的 CI
```

**注意事项**：
- `/loop` 跑在你本地，机器关掉它就停止
- 想不间断运行用 `/schedule` 把它变成云端任务
- 这一层把 Claude Code 变成了**值班机器人**

**轮询频率匹配原则**：轮询频率超过变化频率就是 token 浪费。PR 一小时才有一条 review，就别用 5 分钟轮询。

---

## 第四层：Proactive — 交出整个决策流程

把前面所有原语组合起来，做成无人值守的长期任务流水线。

```bash
/schedule 每小时检查 #project-feedback 里的 bug 报告。
/goal 这一轮发现的每个报告都必须被分类、修复、回复后才能停。
修 bug 时用动态工作流在并行 worktree 里探索三种方案，
再让一个独立 agent 做对抗性审查。
```

**⚠️ 风险最高的一层**：
- 动态工作流一次能起几十个 agent，极其烧 token
- 对大模型性能和你提供的上下文信息有极高要求
- 前阵子不少公司砍员工 Claude 订阅，这种跑法很可能是原因之一

---

## Token 消耗控制策略

| 策略 | 做法 | 原理 |
|------|------|------|
| **选对原语和模型** | 简单任务不需要套 loop，能用便宜模型就别用贵的 | 90% 的任务 turn-based 就够了 |
| **确定性工作写脚本** | 比如填 PDF 表单，写一次脚本以后每次调用 | 跑脚本比让模型推理便宜得多 |
| **先小规模试跑** | 动态工作流先跑 5 个验证，别上来就给 100 个 | 先看消耗和质量再放量 |
| **间隔匹配变化频率** | PR 一小时才有一条 review，别用 5 分钟轮询 | 轮询频率超过变化频率就是浪费 |
| **看消耗明细** | `/usage` 看总量，`/goal` 不带参数看当前 loop 消耗，`/workflows` 看每个 agent | 知道钱花在哪才能省 |

---

## 速查表

| Loop 类型 | 你交出去的 | 适合场景 | 用什么 |
|-----------|-----------|---------|--------|
| Turn-based | 验证步骤 | 探索性任务、一次性修改 | Skill |
| Goal-based | 停止条件 | 有明确完成标准的任务 | `/goal` |
| Time-based | 触发时机 | 周期性工作、监控外部系统 | `/loop`、`/schedule` |
| Proactive | 整个决策流程 | 长期运行的定型工作流 | 以上全部 + 动态工作流 |

---

## 作者建议

> 先从 `/goal` 开始。找一个你每天重复做的事，问自己能不能把"做完了"写成一句可验证的话。能写出来，你就可以从 turn-based 升级到 goal-based 了。这一步收益最大，门槛最低，最能节省人力。至于 `/loop` 和 proactive，等你把 `/goal` 用顺了再说也不迟。

## 延伸阅读

- Claude Code 官方 Loop 博客：https://claude.com/blog/getting-started-with-loops
- Loop Engineering：https://mp.weixin.qq.com/s/QR40uuNa1oxtV5ds3i3Ukw
- Codex /goal：https://mp.weixin.qq.com/s/qwjxsGpMacLNy93g6dz4Aw