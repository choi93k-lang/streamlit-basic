---
name: troubleshooting-consultant
description: >-
  Use this skill when an error occurs or when the user reports an issue during execution.
  It guides the agent to analyze root causes, present straightforward solutions,
  and consult with the user before making any modifications.
---

# Troubleshooting Consultant (에러 분석 및 해결 상담 스킬)

실행 중 에러가 발생하거나 사용자가 오류를 보고했을 때, 안전하고 체계적으로 원인을 파악하고 사용자와 의논하여 해결하는 절차를 따릅니다.

## 워크플로우 단계

### 1. 에러 원인 정밀 분석
- 발생한 에러 메시지(Traceback, 콘솔 로그 등)를 파악합니다.
- 라이브러리 미설치, 버전 비호환, 문법 오류, Streamlit 위젯 제약 등 구체적인 원인을 찾습니다.
- 초보자도 쉽게 이해할 수 있는 일상적인 언어로 이유를 정리합니다.

### 2. 해결 방안 옵션 제시
- **가장 단순하고 직관적인 방법(단순성 우선)**을 최우선 옵션으로 제안합니다.
- 필요한 경우 대안(옵션 A, 옵션 B 등)을 명확하게 구분하여 제시합니다.
- 복잡한 예외 처리(`try-except`)나 난해한 코드는 피합니다.

### 3. 사용자와 의논 및 의견 청취
- **임의로 코드를 수정하거나 실행하지 않습니다.**
- 분석한 원인과 해결 방안을 설명한 뒤, 사용자의 의견과 선호도를 묻습니다.

### 4. 사용자 승인 후 적용 및 검증
- 사용자가 명시적으로 선택하고 승인한 해결책에 맞춰 코드를 수정합니다.
- 수정 완료 후 변경된 내용과 테스트 방법을 안내합니다.
- 변경 사항을 Git에 깔끔하게 커밋합니다.

