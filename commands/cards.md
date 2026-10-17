---
description: 타로 카드 사전 — 78장 카드의 정방향·역방향 의미를 찾아봅니다
argument-hint: "[카드 번호 또는 이름 (비우면 전체 목록)]"
allowed-tools: Bash(python3:*)
---

손님이 타로 카드의 의미를 궁금해해. 아래 규칙에 따라 카드 정보를 찾아 보여줘.

- 인자가 비어 있으면 `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tarot.py" list` 를 실행해 78장 전체를 보여줘.
- 인자가 있으면 `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tarot.py" show <인자>` 를 실행해.
- 결과에 있는 의미만 전하고, 없는 해석을 지어내지 마.
- 타로바 대화 중이었다면 에이닷의 말투로 짧게 설명을 곁들여.

찾을 카드: $ARGUMENTS
