# 华北活动采集 Skill

这是一个跨 AI 工具可复用的活动采集 Skill：入口是 `SKILL.md`，不依赖某一种搜索、浏览器或抓取工具。它面向北京、天津、石家庄、保定的美术展、演出、市集、旧货市场、讲座和工作坊。

目录中的 `references/source-registry.yaml` 是可维护的来源清单；`references/event-contract.md` 定义了核验、去重、变更留痕和可回滚的活动记录规则。

## 在 Codex 中使用

将整个 `north-china-activity-collection` 目录复制到 `~/.codex/skills/`，之后可以直接使用 `$north-china-activity-collection`。

## 在其他 AI 工具中使用

将本目录与任务上下文一同提供给工具，并要求它遵循 `SKILL.md`。如果目标工具不支持 Skill 自动发现，仍可将 `SKILL.md` 作为项目级操作规范加载。

该 Skill 只负责发现、核验、更新和输出活动信息；不代表用户购票、登录内容社区或绕过来源访问限制。
