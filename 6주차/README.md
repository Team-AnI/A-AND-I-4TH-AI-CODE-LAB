# 6주차 · Airflow로 SASRec 학습 파이프라인 만들기

> 노트북에서 "한 번" 학습시키던 5주차 SASRec을, **Airflow**로 자동 실행되는 파이프라인(DAG)으로 묶고 **WandB**로 학습 흐름을 관측합니다. 새 코드를 짜는 주차가 아니라, **이미 가진 코드를 운영 가능한 형태로** 만들어보는 주차입니다.

## 🎯 학습 목표

이번 주차가 끝나면 여러분은 다음 질문에 **자기 언어로** 답할 수 있게 됩니다.

1. DAG·Task·TaskFlow API는 무엇이며, "Workflow as Code"는 노트북 수동 실행과 무엇이 다른가?
2. Task 간 값 전달(XCom)과 의존 관계 선언은 코드의 어떤 부분에서 일어나는가?
3. Airflow(실행)와 WandB(관측)의 역할 분담은 무엇이며, 실험 추적이 print 로그와 다른 점은 무엇인가?

## 🧭 이번 주차의 lab 구조

```
[lab_01 따라하기] ──► [lab_02 전체 설명] ──► [lab_03 확장]
   "이렇게 된다"        "왜 그렇게 되나"        "직접 구현"
   첫 DAG 트리거         같은 DAG 한 줄씩 해설    SASRec + WandB 파이프라인
```

> ⚠️ 이번 주차는 Airflow 특성상 **Colab 노트북이 아니라 DAG 파이썬 파일**로 진행합니다. 실행은 로컬 Docker의 Airflow UI(`localhost:8080`)에서 합니다. 설명(🔬 코드 해설)은 lab_02·03 파일 안의 주석으로 들어 있습니다.

## 📚 실습 구성

| # | 파일 | 역할 | 핵심 키워드 | 실행 방법 |
|---|------|------|-------------|-----------|
| 1 | [`dags/lab_01_pipeline.py`](dags/lab_01_pipeline.py) | 따라하기 — 첫 DAG를 트리거하고 그래프 뷰·로그 관찰 | `DAG`, `@task`, `수동 트리거`, `Task 로그` | Airflow UI에서 `lab01_hello_pipeline` 트리거 |
| 2 | [`dags/lab_02_explain.py`](dags/lab_02_explain.py) | 전체 설명 — 동일 DAG를 한 줄씩 분해(🔬 주석) | `TaskFlow API`, `XCom`, `catchup`, `의존 관계` | 파일을 읽으며 UI에서 `lab02_…` 비교 실행 |
| 3 | [`dags/lab_03_sasrec_pipeline.py`](dags/lab_03_sasrec_pipeline.py) | 확장 — 5주차 SASRec을 DAG로 감싸고 WandB 기록 | `leave-one-out`, `HR@10`, `NDCG@10`, `wandb.init/log` | UI에서 `lab03_sasrec_pipeline` 트리거 → WandB 확인 |

## 🛠 환경 구축 (Docker Compose)

**사전 준비물(미리 해오기):** ① [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치 ② [wandb.ai](https://wandb.ai) 무료 계정 가입 후 API 키 발급

```bash
cd 6주차   # 이 폴더(dags/ 포함)에서 진행

# 1) 공식 docker-compose.yaml 내려받기
curl -LfO https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml

# 2) .env 작성 — 키는 코드가 아니라 환경변수로 관리합니다
cat > .env <<EOF
AIRFLOW_UID=$(id -u)
AIRFLOW_IMAGE_NAME=airflow-sasrec-lab:6
WANDB_API_KEY=발급받은-키
EOF

# 3) docker-compose.yaml의 x-airflow-common: 블록 수정
#    - environment: 아래에 한 줄 추가
#        WANDB_API_KEY: ${WANDB_API_KEY:-}
#    - volumes: 아래에 한 줄 추가 (산출물을 호스트에서 보기 위함, 선택)
#        - ${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data
#    (선택) 예제 DAG를 숨기려면 AIRFLOW__CORE__LOAD_EXAMPLES를 'false'로 변경

# 4) 실습용 이미지 빌드 — 동봉된 Dockerfile(torch·wandb 포함)
#    ※ stdin(`- <`) 방식인 이유: 폴더 경로에 한글("6주차")이 있으면
#      docker compose build / docker build . 가 BuildKit 이슈로 실패하기 때문
docker build -t airflow-sasrec-lab:6 - < Dockerfile

# 5) 초기화 후 기동 → http://localhost:8080 (기본 계정 airflow / airflow)
docker compose up airflow-init
docker compose up
```

> `dags/` 폴더는 이 리포에 이미 들어 있으므로, 같은 폴더에서 `docker compose up`만 하면 세 DAG가 UI에 자동으로 나타납니다.

## 🧭 권장 진행 순서

```
lab_01 (15분)   →   lab_02 (45분)   →   lab_03 (60분+)
"한 번 돌려본다"     "왜 그런지 이해한다"    "직접 굴려본다"
```

1. **lab_01**: `lab01_hello_pipeline`을 수동 트리거 → 그래프 뷰에서 Task가 순서대로 초록색이 되는 과정과 Task 로그를 관찰.
2. **lab_02**: 파일의 🔬 해설을 따라 읽으며 `@dag` 파라미터·XCom·의존 관계 선언의 의미를 내재화.
3. **lab_03**: `lab03_sasrec_pipeline` 트리거 → WandB 대시보드에서 loss·HR@10·NDCG@10 곡선 확인 → **(핵심)** `CONFIG`의 `hidden`·`epochs`를 바꿔 재실행하고 두 run을 겹쳐 비교 → (심화) Task를 일부러 실패시켜 `retries` 동작 관찰.

## 🤖 이 실습을 AI와 함께 공부하는 법

- AI는 **답안지가 아니라 튜터**입니다.
- 에러 로그(UI의 Task Logs)를 그대로 붙여 넣고 "원인 후보를 3개만" 요청해 보세요. 정답을 받기 전에 본인의 가설을 먼저 말하는 것이 원칙입니다.
- lab_03의 WandB 곡선을 보고 "hidden을 키웠더니 왜 이런 변화가 생겼는가"를 자기 언어로 요약한 뒤 AI에게 검증받아 보세요.

## 🧩 이번 주차의 메타 질문 (파인만 기법용)

모든 실습이 끝나면 아래 질문에 **각각 3문장 이내**로 답해 보세요.

1. 친구가 "Airflow가 뭐야?"라고 묻는다면, "노트북 수동 실행"과 대비해 1분 안에 설명할 수 있는가?
2. Airflow와 WandB 중 하나만 쓴다면 각각 무엇을 잃게 되는가? "실행"과 "관측"이라는 단어로 설명하라.
3. 매주 새 데이터로 SASRec을 다시 학습시켜야 한다면, 오늘 만든 파이프라인에서 무엇을 바꾸면 되는가? (`schedule` 한 줄)

## 📦 요구사항

- Docker Desktop, WandB 무료 계정 (위 "환경 구축" 참고)
- 파이썬 패키지(torch, wandb)는 동봉된 [`Dockerfile`](Dockerfile)로 이미지에 설치되므로 로컬 설치는 필요 없습니다.
- MovieLens 100K는 DAG 첫 실행 시 자동 다운로드됩니다. 1M으로 바꾸려면 `lab_03` 상단의 `DATA_URL` 주석을 교체하세요.

## 📚 참고 문헌

- **Apache Airflow 공식 튜토리얼** — DAG 작성 기초부터 TaskFlow API까지. [airflow.apache.org/docs/apache-airflow/stable/tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/)
- **Running Airflow in Docker** — 공식 Docker Compose 가이드. [docker-compose 가이드](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- **Astronomer Learn** — *Manage your ML models with Weights and Biases and Airflow*. 이번 실습과 같은 구조의 공식 튜토리얼. [astronomer.io/docs/learn/airflow-weights-and-biases](https://www.astronomer.io/docs/learn/airflow-weights-and-biases/)
- **Weights & Biases Quickstart** — `wandb.init`/`wandb.log` 기본 사용법. [docs.wandb.ai/quickstart](https://docs.wandb.ai/quickstart)
- **Kang & McAuley (2018)** — *Self-Attentive Sequential Recommendation* (SASRec). [arxiv.org/abs/1808.09781](https://arxiv.org/abs/1808.09781)

---

다음 주(7주차)는 **논문 탐색 및 발표**입니다. 오늘 파이프라인으로 "굴려본" SASRec의 원논문을 직접 읽고 정리하는 것이 자연스러운 출발점이 됩니다.
