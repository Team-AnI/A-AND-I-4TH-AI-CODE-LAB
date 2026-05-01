# 3주차 · MNIST로 데이터 파이프라인 익히기

> 모델보다 먼저 **데이터를 다루는 감각**을 기릅니다. EDA → 전처리 → 특징 공학(증강)의 한 흐름을 직접 손으로 만들어 봅니다.

## 🎯 학습 목표

이번 주차가 끝나면 여러분은 다음 질문에 **자기 언어로** 답할 수 있게 됩니다.

1. 새 데이터셋을 받았을 때, **모델을 짜기 전에** 먼저 무엇을 살펴봐야 하는가?
2. 픽셀을 0~255 그대로 모델에 넣으면 왜 안 되는가? `Normalize`의 두 숫자(0.1307, 0.3081)는 어디서 나오는가?
3. 데이터 증강(augmentation)을 **학습 데이터에만** 적용해야 하는 이유는 무엇인가?

## 🧭 이번 주차의 lab 구조 

```
[lab_01 Overview] ──► [lab_02 Explained] ──► [lab_03 Apply]
   "이렇게 된다"         "왜 그렇게 되나"          "변화 적용"
   전체 코드 실행        한 줄씩 분해 설명         EDA, 전처리, 특징 공학
```

세 lab을 **순서대로** 보아야 의미가 통합니다.

## 📚 실습 구성

| # | 파일 | 역할 | 핵심 키워드 | 설명 | Colab |
|---|------|------|-------------|------|-------|
| 1 | [`lab_01_pipeline.ipynb`](lab_01_pipeline.ipynb) | Overview — 전체 파이프라인 한 번에 실행 | `datasets.MNIST`, `transforms`, 시각화 | 📖 설명 없음| [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Team-AnI/A-AND-I-4TH-AI-CODE-LAB/blob/main/3주차/lab_01_pipeline.ipynb) |
| 2 | [`lab_02_explain.ipynb`](lab_02_explain.ipynb) | Explain — 같은 코드를 한 줄씩 분해 | `(C,H,W)`, `Normalize`, `Compose`, 증강 원리 | 📖 설명 없음 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Team-AnI/A-AND-I-4TH-AI-CODE-LAB/blob/main/3주차/lab_02_explain.ipynb) |
| 3 | [`lab_03_apply.ipynb`](lab_03_apply.ipynb) | Apply — EDA, 전처리, 특징 공학 | 평균 이미지, 수동 정규화, 커스텀 transform | 📖 설명 없음 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Team-AnI/A-AND-I-4TH-AI-CODE-LAB/blob/main/3주차/lab_03_apply.ipynb) |

> **Colab으로 실행하는 법:** 표의 **Open in Colab** 배지를 누르면 해당 노트북이 **여러분 Google 계정의 Colab**에서 열립니다. 실행·사용량은 각자 본인 계정 기준이며, 수정본을 남기려면 `파일 → Drive에 사본 저장` 하세요. GPU는 이번 주차에는 필수가 아닙니다.

## 🧭 권장 진행 순서

```
lab_01 (15분)   →   lab_02 (45분)   →   lab_03 (60분+)
"한 번 돌려본다"     "왜 그런지 이해한다"    "직접 짜본다"
```

각 실습은 아래 비율로 진행하세요.

1. **lab_01**: 셀을 위에서 아래로 한 번 실행. 결과 그림 눈으로 확인.
2. **lab_02**: 한 셀씩 천천히 읽고, 각 코드 옆 설명과 "직접 해보기"·AI 5단계 프롬프트로 내재화.
3. **lab_03**: EDA, 전처리, 특징 공학의 내용을 확인.

## 🤖 이 실습을 AI와 함께 공부하는 법

3주차의 AI 활용은 **lab_02·03에 집중**되어 있습니다.

- **lab_02** — 5단계 프롬프트(구조화 → 회상 → 비교/검증 → 연결 → 파인만) 풀세트
- **lab_03** — 응용 단계이므로 Phase 3(비교/검증)·Phase 4(연결)·Phase 5(파인만)만

원칙은 2주차와 같습니다: **AI는 답안지가 아니라 튜터.**

## 🧩 이번 주차의 메타 질문 (파인만 기법용)

모든 실습이 끝나면 아래 3개 질문에 **각각 3문장 이내**로 답해 보세요.

1. 친구가 "MNIST 모델을 왜 그렇게까지 전처리해야 해? 그냥 픽셀 넣으면 안 돼?" 라고 묻는다면, 1분 안에 어떻게 설득하겠는가?
2. `Normalize((0.1307,), (0.3081,))` 의 두 숫자가 다른 데이터셋(예: Fashion-MNIST)에서는 왜 다른 값이 나오는가?
3. 같은 회전 증강(`RandomRotation(5)`)을 학습 데이터에는 적용하고 테스트 데이터에는 적용하지 않는 이유를, "공정한 평가" 라는 키워드로 설명해 보라.

## 📦 요구사항

```bash
pip install torch torchvision matplotlib numpy
```

Colab에는 모두 기본 설치되어 있습니다. MNIST는 첫 실행 시 자동 다운로드(~10MB).

## 📚 참고 문헌

- **LeCun et al. (1998)** — *Gradient-Based Learning Applied to Document Recognition*. MNIST 데이터셋의 28×28 규격, 60k/10k 분할, 10개 클래스 구성의 출처.
- **Ioffe & Szegedy (2015)** — *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*. 입력 분포가 학습 안정성에 미치는 영향(Internal Covariate Shift) — 전처리에서 정규화를 하는 이론적 배경의 한 축.
- **An et al. (2020)** — *An Ensemble of Simple CNN Models for MNIST Digit Recognition*. MNIST에서 회전·이동 증강의 실험적 효과 보고.
