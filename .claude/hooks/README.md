# Claude Code Hooks — VSteach

本目录存放项目级的 Claude Code 钩子脚本。

## 可用钩子

| 钩子 | 触发时机 | 文件 |
|------|----------|------|
| `preToolUse` | 每次调用工具前 | 配置在 `settings.json` |
| `postToolUse` | 每次调用工具后 | 配置在 `settings.json` |
| `preMessage` | 每次用户消息前 | 配置在 `settings.json` |
| `postMessage` | 每次回复后 | 配置在 `settings.json` |

## 当前配置

### preToolUse (Bash)
自动切换到 VSteach 工作目录，确保所有命令在正确路径下执行。

配置位置：`.claude/settings.json → hooks.preToolUse.Bash.command`

## 添加新钩子

1. 在 `settings.json` 的 `hooks` 下添加对应条目
2. command 可以是内联命令或脚本路径
3. Windows 下使用 `.bat` 或直接写命令

示例：
```json
{
  "hooks": {
    "postToolUse": {
      "Bash": {
        "command": "echo [Hook] Bash tool used >> .claude/hooks/usage.log"
      }
    }
  }
}
```