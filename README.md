# AI-code-lab

본 과정은 인공지능에 대한 기초적인 이해를 넘어, 실제 AI 모델을 직접 구성하고 활용하는 역량을 기르는 것을 목표로 설계된 심화 과정입니다. 단순히 이론을 습득하는 데 그치지 않고, 코드 실습과 개념 이해를 반복적으로 연결함으로써 기술을 내재화할 수 있도록 구성되어 있습니다.

## 커리큘럼

| 순서 | 유형 | 주제 | 핵심 키워드 |
|------|------|------|-------------|
| 1 | OT | 오리엔테이션 | 학습 목표·도구 소개 |
| 2 | 영상 | PyTorch | Tensor, Autograd, Training Loop |
| 3 | 실습 | MNIST — EDA, 전처리, 특징 공학 | Dataset, DataLoader, Feature Engineering |
| 4 | 실습 | MovieLens — Collaborative Filtering | Embedding, Cosine Similarity, User/Item Matrix, MF |
| 5 | 실습 | MovieLens — SASRec | Attention, Transformer, Sequential Recommendation |
| 6 | 실습 | Airflow | DAG, Scheduling, Operators, Pipeline, Orchestration |
| 7 | 심화 | 논문 조사 및 발표 | Paper Research, Presentation |
| 8 | 프로젝트 | 기초 프로젝트 | End-to-End 구현 |
| 9 | 팀 프로젝트 | 팀 프로젝트 | 협업, 배포 |

각 주차 폴더(`N주차/`) 안에는 `README.md`, 실습 노트북(`.ipynb`), 실습별 설명(`.md`)이 함께 들어 있습니다.

## 공통 요구사항

```bash
pip install torch torchvision matplotlib numpy pandas
```

각 주차는 **Google Colab**에서 바로 실행할 수 있도록 구성되었습니다.

## 리포지토리 구조

```
AI-code-lab/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── 2주차/
│   ├── README.md
│   ├── lab_01_*.ipynb / .md
│   └── ...
├── 3주차/
└── ...
```

## AI와 협업

`AGENTS.md` 파일 구성을 통해 `Claude`, `Codex`, `Gemini` 등 AI Tool 연동 용이성을 확보했습니다.

## 전체적인 흐름

본 과정은 PyTorch로 모델을 직접 구현하는 것에서 시작하여, 데이터를 정제하고, 의미를 벡터로 표현하고, 이를 추천 시스템에 적용하고, 나아가 실제 서비스로 자동화하는 전체 흐름을 아우릅니다. 각 단계가 이전 학습 내용과 유기적으로 연결되도록 설계되어 있으므로, 순서에 따라 차근차근 학습하시면 AI 시스템의 전체 구조를 온전히 이해하실 수 있을 것입니다.