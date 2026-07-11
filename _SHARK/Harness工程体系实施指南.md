# VSteach · Harness 工程体系实施指南

> **目标**：将 AI 编程从"碰运气"变成"可控可管"的工程体系。
> **演进路径**：提示词工程 → 上下文工程 → **Harness 工程**
> **核心**：把传统软件工程的管理方法，复用到 AI 开发流程中。

---

## 一、五条核心方法

| # | 方法 | 一句话 | 对应传统工程 |
|---|------|--------|-------------|
| 1 | **提前写好规则文件** | 给 AI 划边界 | 项目章程 / 编码规范 |
| 2 | **先方案后编码** | 确认再动手 | 设计评审 / 技术方案 |
| 3 | **MCP + Skills 配工具** | 给 AI 装技能包 | 工具链 / 脚手架 |
| 4 | **自动测试验证** | 写完后跑通 | CI/CD / 自动化测试 |
| 5 | **文档+Git 存档** | 每功能一提交 | 版本控制 / 变更记录 |

### 详细解释

**方法 1：提前写好 AGENTS.md/CLAUDE.md 规则文件**
在项目启动前就把项目背景、技术栈、代码规范全部写进规则文件，从源头给 AI 明确开发边界，避免后续出现乱改技术选型、代码风格混乱的问题。

**方法 2：先让 AI 输出完整方案并人工确认，再动手写代码**
不直接丢需求让 AI"一把梭"开发，先通过 Plan 模式让 AI 输出全流程开发计划，人工核对砍掉冗余功能、调整开发优先级，确认无误后再进入编码环节，大幅减少后续返工。

**方法 3：用 MCP 和 Skills 给 AI 配齐工具能力**
给 AI 接入 MCP 协议扩展操作权限，搭配封装好的专业技能包，让 AI 可以自主联网查资料、获取最新的官方文档，不用依赖过时的知识库内容写代码。

**方法 4：功能开发完成后必须让 AI 自行跑通测试验证**
代码写完后不直接交付，让 AI 自动执行 Lint 检查、运行自动化测试用例，甚至自主打开浏览器操作验证功能，确认全流程正常可用，从流程上避免"表面写完实际全是 Bug"的情况。

**方法 5：每完成一个功能就让 AI 沉淀文档并提交代码**
每做完一个模块就同步更新项目进度文档，同时用 Git 提交代码生成"存档点"，哪怕后续 AI 迭代出问题，也能随时回滚到之前的稳定版本，避免整个项目失控。

---

## 二、当前实施状态

### ✅ 已完成

| 方法 | 条目 | 位置 |
|------|------|------|
| ① | CLAUDE.md 补充 AI 开发规则 | `CLAUDE.md` → `## AI 开发规则` |
| ② | 固化"先方案后编码"流程 | `CLAUDE.md` → 工作流程 |
| ③ | 配置 MCP 服务器（Playwright + Sequential Thinking + Context7） | settings.json |
| ③ | 创建 chris-daily-plan Skill | `.claude/skills/chris-daily-plan/SKILL.md` |
| ④ | 创建项目验证脚本 | `_test/run_verify.py` |
| ④ | 创建 hooks 文档 | `.claude/hooks/README.md` |
| ⑤ | 固化 git 提交规范 | `CLAUDE.md` → 版本控制 |
| — | settings.json 权限白名单 | `.claude/settings.json` → `permissions.allow` |

### ⏳ 待实施

| # | 项目 | 触发条件 | 预计耗时 |
|---|------|----------|----------|
| A | 定型文稿挑战书 Skill | 下次执行复杂开发任务前 | 15 分钟 |
| B | Git pre-commit 自动验证钩子 | 确认 git hooks 目录无干扰 | 10 分钟 |
| C | 项目 README.md | 项目需公开/分享时 | 20 分钟 |
| D | 联网搜索 MCP（Brave Search） | 需要 AI 自主搜索资料时 | 30 分钟（含注册 API Key） |
| E | 各子目录 README | 项目规模继续扩大时 | 15 分钟 |
| F | 完善 .gitignore | 出现多余文件被跟踪时 | 5 分钟 |
| G | 备份自动化 hook | OneDrive 备份路径确认后 | 10 分钟 |

---

## 三、使用 Superpowers 实现 Harness 工程

> Superpowers 是一个开源的 AI 编程方法论插件，内置了一整套 Skill，**天然对应 Harness 五条方法**。已安装于本环境（`~/.claude/plugins/`）。

### 方法对照表

| Harness 方法 | Superpowers 对应的 Skill | 作用 |
|:---|:---|:---|
| ① 规则文件 | `CLAUDE.md` / `AGENTS.md` | 项目级指令，Superpowers 的 `CLAUDE.md` 和 `AGENTS.md` 本身就是最佳实践范例 |
| ② 先方案后编码 | **`brainstorming`** + **`writing-plans`** | `brainstorming` 自动启动，通过问答细化需求，输出设计文档；`writing-plans` 将设计拆解为 2-5 分钟的可执行任务 |
| ③ MCP + Skills | **`using-superpowers`** | 引导 AI 识别并使用所有已安装的 Skill 和 MCP |
| ④ 自动测试验证 | **`test-driven-development`** + **`verification-before-completion`** | TDD 强制 RED-GREEN-REFACTOR 循环；`verification-before-completion` 确认真实修复 |
| ⑤ 文档+Git 存档 | **`finishing-a-development-branch`** | 验证测试 → 提供合并/PR/保留/丢弃选项 → 清理工作区 |

### 安装 Superpowers

```bash
# 如果尚未安装：
/plugin install superpowers@claude-plugins-official
/reload-plugins
```

安装后，Superpowers 的 Skill 会在对应场景自动触发，无需手动调用。

### 使用流程

当启动一个新功能开发时，Superpowers 的自动工作流：

```
你提出需求
  → brainstorming 自动启动，追问澄清需求
  → 输出设计文档供你确认
  → writing-plans 将需求拆解为可执行任务清单
  → subagent-driven-development 逐个执行任务
    → 每个任务：子代理实现 → 跑测试 → 代码审查
  → requesting-code-review 整体审查
  → finishing-a-development-branch 提交代码
```

---

## 四、多 Agent 协作实战

### 4.1 什么是多 Agent 协作

多 Agent 协作是指让**多个独立的 Claude 实例**并行工作，每个负责一个子任务，互不干扰。

```
┌─ 主会话（你） ─────────────────────────────┐
│  负责：需求分解、协调、质量把关              │
│                                             │
│  ┌─ Agent A ─┐  ┌─ Agent B ─┐  ┌─ Agent C ─┐│
│  │ 写模块1    │  │ 写模块2    │  │ 写测试    ││
│  │ 独立上下文 │  │ 独立上下文 │  │ 独立上下文 ││
│  └────────────┘  └────────────┘  └────────────┘│
└─────────────────────────────────────────────────┘
```

### 4.2 什么时候用多 Agent

| 适合 | 不适合 |
|------|--------|
| 多个独立模块可以并行开发 | 代码高度耦合，改一处影响全局 |
| 多个独立的 Bug 需要修复 | Bug 之间存在依赖关系 |
| 需要同时查不同方向的资料 | 探索性任务，方向未定 |
| 代码实现 + 测试用例可以分开写 | 资源受限（Token 预算有限） |

### 4.3 Superpowers 的多 Agent 方案

**方案 A：subagent-driven-development（推荐）**
主会话内启动子代理，每个子代理完成一个任务后立即审查，适合同一项目内的多任务并行：

```bash
# Superpowers 自动使用此模式，无需手动操作
# 主会话生成 plan → 自动调度 implementer 子代理 → task reviewer 审查
```

**方案 B：dispatching-parallel-agents（独立并行）**
同时启动多个独立 Agent，各自完成互不相关的任务：

```
适用场景：
- 同时查多个 API 文档
- 多个独立模块分别实现
- 并行修复不同子系统的 Bug
```

### 4.4 手工实现多 Agent 协作

如果不想依赖 Superpowers，可以手动操作：

**方式 1：同一会话中手工调度（最简单）**
```markdown
在 Prompt 中明确指定：
"先用 Agent A 分析方案，再用 Agent B 审查方案，
两个独立进行，最后汇总结果"
```

**方式 2：Worktree 隔离（适合大型任务）**
```bash
claude --worktree           # 创建隔离工作区
claude agents               # 查看所有运行中的会话
```

**方式 3：Workflow 脚本（最强大）**
使用 Claude Code 的 Workflow 功能编排多个子代理：
```javascript
// .claude/workflows/并行开发.js
const results = await parallel([
  () => agent("实现模块A的...", { schema: SCHEMA }),
  () => agent("实现模块B的...", { schema: SCHEMA }),
])
```

---

## 五、Harness 规则清单（未来使用指引）

> **当遇到以下场景时，请参考对应的规则进行实施。**

### 规则 1：启动新项目时

```
□ 创建 CLAUDE.md（项目背景 + 技术栈 + 代码规范）
□ 配置 .claude/settings.json（权限白名单）
□ 创建 _test/ 目录 + 验证脚本
□ 初始化 Git 仓库
□ （可选）安装 Superpowers：/plugin install superpowers@claude-plugins-official
```

### 规则 2：开始新功能开发时

```
□ 先方案后编码：让 AI 输出完整方案，人工确认
□ 如有独立子任务 → 考虑多 Agent 并行
□ 写测试用例 → 再写实现代码（TDD）
□ 实现后跑通所有测试
□ 更新相关文档
□ Git 提交（规范格式）
```

### 规则 3：需要 MCP 扩展能力时

```
□ 先判断：Claude 现有能力是否已够用？
□ 如果需要联网 → Brave Search / Tavily MCP
□ 如果需要浏览器操作 → Playwright MCP
□ 如果需要查实时文档 → Context7 MCP
□ 如果需要分步推理 → Sequential Thinking MCP
□ 如果需要数据库操作 → 对应数据库 MCP
```

### 规则 4：代码审查时

```
□ 使用 /code-review 自动审查当前改动
□ 关注：正确性 > 性能 > 代码风格
□ 高风险改动：让 AI 打开浏览器验证功能
□ 验证不通过 → 不允许提交
```

### 规则 5：项目维护时

```
□ 定期运行验证脚本
□ 定期清理 __temp/ 目录
□ 提交信息保持规范格式
□ 功能完成即同步更新文档
□ 检查 Git 是否有未提交的改动
```

---

## 六、实施决策树

```
开始新任务
│
├─ 是全新项目？
│   → 执行规则 1（初始化项目基建）
│
├─ 是现有项目的新功能？
│   ├─ 已有 CLAUDE.md？ → 执行规则 2（方案→编码→验证→提交）
│   └─ 没有规则文件？  → 先写 CLAUDE.md，再执行规则 2
│
├─ 需要新能力（联网/浏览器/数据库）？
│   → 执行规则 3（添加对应 MCP）
│
├─ 收到代码变更需要审查？
│   → 执行规则 4（审查→验证→通过）
│
└─ 日常维护？
    → 执行规则 5（检查状态）
```

---

## 七、三层演进对照

| 层级 | 之前的状态 | 现在 | 下一个目标 |
|------|-----------|------|----------|
| 提示词工程 | CLAUDE.md 教学原则 | ✅ 已完善 | — |
| 上下文工程 | 每次手动说明 | ✅ rules + hooks 自动加载 | 定型文稿挑战书 Skill |
| **Harness 工程** | 无完整体系 | ✅ settings + verify + MCP + 5 方法 | pre-commit 钩子 + README + 多 Agent 工作流 |

---

## 八、快速检查清单

每次对话时可快速检查：

- [ ] `python _test/run_verify.py` — 验证脚本能跑通
- [ ] `.claude/settings.json` — 权限/MCP/钩子配置正常
- [ ] 当前工作是否遵循"先方案后编码"
- [ ] 最近一次 git 提交是否符合规范
- [ ] `__temp/` 是否有需要清理的文件
- [ ] 当前任务是否需要多 Agent 并行

---

*最后更新：2026-07-09*
*下次审查：有新功能或项目规模变化时*