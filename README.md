<p align="center">
  <img src="assets/brand/mindie-agent-logo.png" alt="MindIE Agent logo" width="128" height="128">
</p>

# MindIE Agent

通过领域上下文、稳定的远端工具，以及知识与经验反馈闭环，帮助 Agent 完成 Ascend 开发任务。

**0.0.1 产品入口：[Codex](https://github.com/mindie-agent/mindie-agent-codex) 与 [Claude Code](https://github.com/mindie-agent/mindie-agent-cc)。**
在自己的业务仓库和原生任务中使用插件。安装沿用已有贡献选择和项目范围，合格任务内部自动关联，不增加日常激活或收尾步骤。完整公开正文由本地程序筛选、脱敏并保存；内部小模型生成必要检索导航，不能替代正文。尚未选择贡献时不采集，缺配置与明确停用分别报告。远端通过 remote-dev 提供执行环境。

## 当前进展

首发 `0.0.1` 为普通内测 Release，覆盖 Codex / Claude Code 与 macOS、
原生 Windows、Windows WSL 六个组合。[发布记录](docs/releases/0.0.1.md)
集中说明精确支持版本、各组合证据和已知问题。Codex 子代理被中断后，待完成的
工具调用或远端命令可能继续运行；该限制不阻塞首发，不增加插件补偿机制。
benchmark 独立推进，本次不宣称任务质量或成本收益。
[用户须知](https://github.com/mindie-agent/mindie-agent-codex/blob/main/plugins/mindie-agent/skills/mindie-agent/references/user-notice.md)
说明完整材料、规则脱敏与公开 Git 历史，不增加新的授权步骤。

首个领域为 vLLM / vLLM-Ascend。完整材料、检索导航与公开任务包的设计见
[系统性设计](docs/systematic-knowledge-design-2026-10-04.md)。
精确提交和验证范围见[实施进度](docs/implementation-status.md)；开发候选、
已合入版本、原生宿主与公开发布证据分别记录。

Kimi 保留独立适配器和历史证据，不在此次首发范围。

## 仓库分工

| 仓库 | 职责 |
|---|---|
| [mindie-agent](https://github.com/mindie-agent/mindie-agent) | 架构、领域边界与交付入口 |
| [mindie-agent-codex](https://github.com/mindie-agent/mindie-agent-codex) | Codex Plugin、Hook 和原生任务接入 |
| [mindie-agent-kimi](https://github.com/mindie-agent/mindie-agent-kimi) | Kimi 原生插件、Hook、任务身份和本地模型适配 |
| [mindie-agent-cc](https://github.com/mindie-agent/mindie-agent-cc) | Claude Code 原生插件、Hook、任务身份和本地模型适配 |
| [knowledge](https://github.com/mindie-agent/knowledge) | 共享知识与经验运行时、可选贡献、分发和反馈 |
| [knowledge-vllm-ascend](https://github.com/mindie-agent/knowledge-vllm-ascend) | vLLM-Ascend 领域内容 |
| [remote-dev](https://github.com/mindie-agent/remote-dev) | 远端文件、命令、作业与产物 |
| [coordinator](https://github.com/mindie-agent/coordinator) | 受管环境、资源与执行 |
| [diagnostics](https://github.com/mindie-agent/diagnostics) | 组件诊断 |
| [npu-top](https://github.com/mindie-agent/npu-top) | 可选 NPU 观测 |

当前正式 feed 是 [knowledge-vllm-ascend/main](https://github.com/mindie-agent/knowledge-vllm-ascend/tree/main)。
插件首次安装固定 `v0.0.1`，按各产品仓库说明通过原生市场安装。
后续在上次成功检查超过 24 小时后的自然使用中异步检查，后台准备当前
Harness 支持的最高正式 Release，空闲时生效；更新不重新询问已有授权。

## 架构与下一步

[当前架构](docs/architecture.md)遵循[设计原则](docs/design-principles.md)，[后续迭代](docs/next-steps.md)在本仓库维护。[Issue #195](https://github.com/mindie-agent/mindie-agent/issues/195)保留早期设计讨论。
一会话一个主要领域，用户持续直接指导；跨域使用同一 Harness 中可直接交互的独立任务。

后续持续验证实际业务复用收益，并跟进已知宿主限制；旧业务 Skill 与 profiling 暂缓。
所有设计取舍优先遵守九条原则，常规任务不承担额外强制流程。

本仓库由 VAWS 原地更名，保留正常 Git 历史和既有材料。
旧 workspace/bootstrap、源码托管、自动更新器、客户端 Hook/MCP 接线与自动加载的业务 Skill 已从当前树删除。
各组件直接使用新包名、导入名和配置，不提供旧名别名或旧安装通道。
业务方法后续按领域重新整理进插件与知识库，旧实现仅保留在 Git 历史中。
历史验证只证明其记录的版本与范围。

[English](README.en.md)
