# 4주차 · MovieLens로 협업 필터링 익히기

> 사용자들의 **행동 데이터**만으로 추천을 만드는 협업 필터링을 직접 구현합니다. User-based CF → Item-based CF의 흐름을 따라가며, 추천 시스템의 핵심 아이디어와 한계를 손으로 체험합니다.

## 🎯 학습 목표

이번 주차가 끝나면 여러분은 다음 질문에 **자기 언어로** 답할 수 있게 됩니다.

1. User-based CF와 Item-based CF는 어떤 차이가 있으며, 실제 대규모 서비스에서는 어떤 방식이 더 자주 쓰이는가?
2. 코사인 유사도가 "나와 비슷한 사용자"를 찾는 데 어떻게 쓰이는가? 평점 벡터와 임베딩 벡터의 관계는 무엇인가?
3. 협업 필터링의 두 가지 구조적 한계(희소성, 콜드 스타트)는 왜 발생하는가?

## 🧭 이번 주차의 lab 구조

```
[lab_01 Overview] ──► [lab_02 Explained] ──► [lab_03 Apply]
   "이렇게 된다"         "왜 그렇게 되나"          "직접 구현"
   User-based CF         코사인 유사도 복습         EDA + Item-based CF
   전체 코드 실행         한 줄씩 분해 설명          희소성 시각화 + 구현
```

세 lab을 **순서대로** 보아야 의미가 통합니다.

## 📚 실습 구성

| # | 파일 | 역할 | 핵심 키워드 | 설명 | Colab |
|---|------|------|-------------|------|-------|
| 1 | [`lab_01_pipeline.ipynb`](lab_01_pipeline.ipynb) | Overview — User-based CF 전체 파이프라인 실행 | `User-Item 행렬`, `코사인 유사도`, `이웃 선정`, `추천` | 📖 설명 없음 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Team-AnI/A-AND-I-4TH-AI-CODE-LAB/blob/main/4주차/lab_01_pipeline.ipynb) |
| 2 | [`lab_02_explain.ipynb`](lab_02_explain.ipynb) | Explain — 코사인 유사도부터 CF 코드 한 줄씩 분해 | `임베딩`, `F.cosine_similarity`, `희소성`, `콜드 스타트` | 📖 설명 없음 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Team-AnI/A-AND-I-4TH-AI-CODE-LAB/blob/main/4주차/lab_02_explain.ipynb) |
| 3 | [`lab_03_apply.ipynb`](lab_03_apply.ipynb) | Apply — EDA, Sparsity 시각화, Item-based CF 구현 | `평점 분포`, `희소 행렬`, `아이템 유사도`, `Item-based CF` | 📖 설명 없음 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Team-AnI/A-AND-I-4TH-AI-CODE-LAB/blob/main/4주차/lab_03_apply.ipynb) |

> **Colab으로 실행하는 법:** 표의 **Open in Colab** 배지를 누르면 해당 노트북이 **여러분 Google 계정의 Colab**에서 열립니다. 실행·사용량은 각자 본인 계정 기준이며, 수정본을 남기려면 `파일 → Drive에 사본 저장` 하세요. MovieLens 데이터는 첫 실행 시 자동 다운로드됩니다.

## 🧭 권장 진행 순서

```
lab_01 (15분)   →   lab_02 (45분)   →   lab_03 (60분+)
"한 번 돌려본다"     "왜 그런지 이해한다"    "직접 짜본다"
```

각 실습은 아래 비율로 진행하세요.

1. **lab_01**: 셀을 위에서 아래로 한 번 실행. 추천 결과를 눈으로 확인.
2. **lab_02**: 한 셀씩 천천히 읽고, 각 코드 옆 설명과 AI 5단계 프롬프트로 내재화.
3. **lab_03**: EDA로 데이터를 파악한 뒤, Item-based CF를 단계별로 구현.

## 🤖 이 실습을 AI와 함께 공부하는 법

4주차의 AI 활용은 **lab_02·03에 집중**되어 있습니다.

- **lab_02** — 5단계 프롬프트(구조화 → 회상 → 비교/검증 → 연결 → 파인만) 풀세트
- **lab_03** — 응용 단계이므로 Phase 3(비교/검증)·Phase 4(연결)·Phase 5(파인만)만

원칙은 이전 주차와 같습니다: **AI는 답안지가 아니라 튜터.**

## 🧩 이번 주차의 메타 질문 (파인만 기법용)

모든 실습이 끝나면 아래 3개 질문에 **각각 3문장 이내**로 답해 보세요.

1. 친구가 "넷플릭스는 어떻게 내 취향을 아는 거야?" 라고 묻는다면, 협업 필터링 아이디어만으로 1분 안에 설명할 수 있는가?
2. User-based CF를 넷플릭스 규모(수억 명 사용자)에 그대로 적용하면 왜 문제가 생기는가? Sparsity와 Cold Start 중심으로 설명하라.
3. 아마존의 "이 상품을 구매한 고객이 함께 구매한 상품"은 User-based CF인가, Item-based CF인가? 이유와 함께 설명하라.

## 📦 요구사항

```bash
pip install torch pandas numpy matplotlib
```

Colab에는 모두 기본 설치되어 있습니다. MovieLens ml-100k 데이터는 첫 실행 시 자동 다운로드(~5MB).

## 📚 참고 문헌

- **Sarwar et al. (2001)** — *Item-Based Collaborative Filtering Recommendation Algorithms*. WWW10. User-Item 평점 행렬 구조와 Item-based CF의 기초.
- **Koren, Bell & Volinsky (2009)** — *Matrix Factorization Techniques for Recommender Systems*. IEEE Computer. 메모리 기반 CF의 한계(Sparsity, Cold Start)와 Matrix Factorization 등장 배경.
- **Stanford CS246** — *Mining Massive Datasets*, Leskovec 교수 슬라이드. 협업 필터링 구성 흐름 전체를 수치 예제와 함께 설명. [슬라이드 PDF](https://web.stanford.edu/class/cs246/slides/07-recsys1.pdf)
