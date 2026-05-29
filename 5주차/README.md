# 5주차 · Attention, Transformer, SASRec

> 사용자의 **행동 순서**를 모델에 반영하는 순차 추천(Sequential Recommendation)을 배웁니다. 어텐션과 트랜스포머를 라이브러리로 직접 돌려보고, 이를 추천에 적용한 **SASRec**을 MovieLens로 학습시켜 다음 영화를 예측합니다.

## 🎯 학습 목표

이번 주차가 끝나면 여러분은 다음 질문에 **자기 언어로** 답할 수 있게 됩니다.

1. 셀프 어텐션은 시퀀스의 각 위치가 서로를 어떻게 바라보며, 어텐션 가중치 행렬의 한 행은 무엇을 의미하는가?
2. 다음 아이템을 예측할 때 왜 미래를 가려야 하며(causal masking), −∞ → softmax는 어떻게 그것을 구현하는가?
3. 4주차 협업 필터링이 놓친 '순서' 신호를 SASRec은 어떻게 활용하는가?

## 🧭 이번 주차의 lab 구조

```
[lab_01 따라하기] ──► [lab_02 전체 설명] ──► [lab_03 확장]
   "이렇게 된다"        "왜 그렇게 되나"        "직접 구현"
   Attention/Transformer  같은 코드 한 줄씩      SASRec on MovieLens
   라이브러리로 실행       QKV·마스크·인코더 해설   EDA + 학습 + 어텐션 히트맵
```

세 lab을 **순서대로** 보아야 의미가 통합니다.

## 📚 실습 구성

| # | 파일 | 역할 | 핵심 키워드 | 설명 | Colab |
|---|------|------|-------------|------|-------|
| 1 | [`lab_01_attention.ipynb`](lab_01_attention.ipynb) | 따라하기 — 어텐션·트랜스포머를 라이브러리로 한 번에 실행 | `nn.MultiheadAttention`, `Self-Attention`, `Causal Mask`, `TransformerEncoder` | 📖 노트북 내장 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Team-AnI/A-AND-I-4TH-AI-CODE-LAB/blob/main/5주차/lab_01_attention.ipynb) |
| 2 | [`lab_02_explain.ipynb`](lab_02_explain.ipynb) | 전체 설명 — 동일 코드를 한 줄씩 분해 | `Query·Key·Value`, `scaled dot-product`, `positional embedding`, `multi-head` | 📖 노트북 내장 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Team-AnI/A-AND-I-4TH-AI-CODE-LAB/blob/main/5주차/lab_02_explain.ipynb) |
| 3 | [`lab_03_sasrec.ipynb`](lab_03_sasrec.ipynb) | 확장 — SASRec 구현 + EDA + 어텐션 히트맵 | `시퀀스 EDA`, `next-item prediction`, `SASRec`, `attention heatmap` | 📖 노트북 내장 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Team-AnI/A-AND-I-4TH-AI-CODE-LAB/blob/main/5주차/lab_03_sasrec.ipynb) |

> **Colab으로 실행하는 법:** 표의 **Open in Colab** 배지를 누르면 해당 노트북이 **여러분 Google 계정의 Colab**에서 열립니다. 실행·사용량은 각자 본인 계정 기준이며, 수정본을 남기려면 `파일 → Drive에 사본 저장` 하세요. MovieLens 데이터(lab_03)는 첫 실행 시 자동 다운로드되며, GPU가 필요하면 `런타임 → 런타임 유형 변경 → GPU`로 바꾸면 됩니다(CPU로도 1~2분이면 학습됩니다).

## 🧭 권장 진행 순서

```
lab_01 (15분)   →   lab_02 (45분)   →   lab_03 (60분+)
"한 번 돌려본다"     "왜 그런지 이해한다"    "직접 학습시킨다"
```

1. **lab_01**: 셀을 위에서 아래로 한 번 실행. 어텐션 가중치 히트맵과 출력 shape를 눈으로 확인.
2. **lab_02**: 한 셀씩 천천히 읽고, 각 코드 옆 `🔬 코드 해설`로 QKV·마스킹·인코더의 원리를 내재화.
3. **lab_03**: 시퀀스 EDA로 데이터를 파악한 뒤, SASRec을 조립·학습시키고 어텐션이 무엇을 보는지 해석.

## 🤖 이 실습을 AI와 함께 공부하는 법

- AI는 **답안지가 아니라 튜터**입니다.
- 막히면 정답을 베끼기 전에, 자기 언어로 먼저 요약하고("셀프 어텐션은 ~다") AI에게 검증받으세요.
- lab_02의 `🔬 코드 해설`을 읽기 전에, 각 코드가 왜 그렇게 쓰였는지 먼저 추측해 보고 AI와 비교해 보세요.
- lab_03에서는 추천 결과나 어텐션 히트맵을 보고 "모델이 왜 이렇게 예측했을까?"를 AI와 함께 해석해 보세요.

## 🧩 이번 주차의 메타 질문 (파인만 기법용)

모든 실습이 끝나면 아래 질문에 **각각 3문장 이내**로 답해 보세요.

1. 친구가 "넷플릭스는 왜 내가 1화를 보면 2화를 추천해?"라고 묻는다면, 순차 추천 아이디어로 1분 안에 설명할 수 있는가?
2. RNN과 비교했을 때 셀프 어텐션이 가진 장점(장기 의존성 + 병렬 처리)을 마르코프 체인의 한계와 엮어 설명하라.
3. 4주차 협업 필터링과 5주차 SASRec에게 **같은 사용자**를 주면 추천이 달라질 수 있다. 그 이유를 '순서'라는 단어로 설명하라.

## 📦 요구사항

```bash
pip install torch pandas numpy matplotlib
```

Colab에는 모두 기본 설치되어 있습니다. MovieLens ml-100k 데이터(lab_03)는 첫 실행 시 자동 다운로드(~5MB)됩니다.

## 📚 참고 문헌

- **Bahdanau et al. (2014)** — *Neural Machine Translation by Jointly Learning to Align and Translate*. 고정 벡터 병목을 어텐션으로 해결한 출발점. [arxiv.org/abs/1409.0473](https://arxiv.org/abs/1409.0473)
- **Vaswani et al. (2017)** — *Attention Is All You Need*. RNN을 제거하고 셀프 어텐션만으로 시퀀스를 처리한 트랜스포머. [arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- **Kang & McAuley (2018)** — *Self-Attentive Sequential Recommendation* (SASRec). 셀프 어텐션을 추천에 적용한 모델. [arxiv.org/abs/1808.09781](https://arxiv.org/abs/1808.09781)
- **Sun et al. (2019)** — *BERT4Rec*. 양방향 어텐션을 추천에 적용한 후속 모델. [arxiv.org/abs/1904.06690](https://arxiv.org/abs/1904.06690)
- **Jay Alammar** — *The Illustrated Transformer*. 그림으로 보는 트랜스포머 입문(QKV·멀티헤드·위치 인코딩). [jalammar.github.io/illustrated-transformer](https://jalammar.github.io/illustrated-transformer/)
- **Stanford CS224N** — *Self-Attention and Transformers*. 슬라이드·강의 영상 공개. [web.stanford.edu/class/cs224n](https://web.stanford.edu/class/cs224n/)
