---
id: decision.project.P-0007
title: "Передача памяти сессии агента в HYAI через MCP на любой машине"
type: decision
status: review
authority: contract
visibility: internal
scope: project
affects_domains: [kit, software, docs, narrative]
affects:
  - "HYAI/core/kernel/agents.md"
  - "AGENTS.md"
supersedes: null
---

# P-0007. Передача памяти сессии агента в HYAI через MCP

## Решение

Агент, работающий на любой машине через MCP, передаёт свой файл памяти сессии `memory/<agent_id>/session-setup.md` в HYAI до начала работы и после каждой значимой записи. Учётные данные из `creds/` в передачу не входят.

## Почему

Чат закрывают и открывают заново, поэтому контекст сессии должен переживать смену чата и машины. Владелец одобрил правку ядра (ответ от этой сессии).

## Границы

- Решение касается всех доменов, поэтому живёт в `project/` (`HYAI-DEC-02`).
- Адрес и ключ MCP не описаны в решении. Они задаются в `creds/`.
- Статус `review`: применение ждёт настройки MCP. Ключ берётся из `MCP_API_KEY` или `creds/mcp`, адрес передаётся параметром `--url` скрипта `vm/mcp_call.py`.

## Открытые вопросы

- `Q-P7-01`: кто передаёт ключ MCP в `creds/mcp` (или `MCP_API_KEY`).
