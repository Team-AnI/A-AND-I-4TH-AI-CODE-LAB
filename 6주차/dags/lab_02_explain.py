"""실습 2: 첫 Airflow DAG Explained (한 줄씩 분해하기)

lab_01과 완전히 동일한 파이프라인입니다. 각 부분에 붙은
`🔬 코드 해설` 주석을 따라 읽으며, 코드가 "왜" 그렇게 작성되었는지
이해하는 것이 목표입니다. UI에는 `lab02_hello_pipeline_explained`로
나타나며, 동작은 lab_01과 같습니다.

[개념 복기 및 이론 점검 — 읽기 전에 스스로 답해 보세요]
- DAG와 Task는 무엇이고, "순환이 없다(Acyclic)"는 조건은 왜 필요할까요?
- @task 함수의 반환값은 어떻게 다음 Task로 전달될까요? (XCom)
- 무거운 라이브러리 import를 함수 안에 두는 이유는 무엇일까요?
"""
from datetime import datetime

from airflow.decorators import dag, task

# ── 🔬 코드 해설: 모듈 상단 ─────────────────────────────────────────
# - `from airflow.decorators import dag, task`: TaskFlow API입니다.
#   파이썬 함수에 데코레이터만 붙이면 DAG와 Task가 되는, Airflow의
#   최신 표준 작성법입니다 ("Workflow as Code").
# - 상단에는 가벼운 import만 둡니다. Scheduler는 이 파일을 주기적으로
#   다시 읽어 DAG 구조를 파악하는데, 무거운 import가 상단에 있으면
#   "구조 파악"만 하는 데에도 그 import가 매번 실행되기 때문입니다.
# ───────────────────────────────────────────────────────────────────

DATA_URL = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
DATA_DIR = "/opt/airflow/data"

# ── 🔬 코드 해설: 경로 상수 ─────────────────────────────────────────
# - Task는 각자 독립된 프로세스에서 실행되므로, 메모리의 변수가 아니라
#   "파일 경로" 같은 작은 값으로 결과 위치를 주고받습니다.
# - `/opt/airflow/data`는 컨테이너 안의 경로입니다. docker-compose에
#   볼륨을 추가하면 호스트의 `./data` 폴더와 연결되어 밖에서도 보입니다.
# ───────────────────────────────────────────────────────────────────


@dag(
    schedule=None,  # 실습에서는 UI에서 수동 트리거
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["recsys", "lab02"],
)
# ── 🔬 코드 해설: @dag 파라미터 ─────────────────────────────────────
# - `schedule=None`: 크론식(예: "0 3 * * *")을 넣으면 주기 실행되지만,
#   이번 실습은 UI의 ▶ 버튼으로 직접 트리거합니다.
# - `start_date`: 이 DAG가 "언제부터 유효한가"의 기준 시각입니다.
# - `catchup=False`: start_date부터 오늘까지의 과거 구간을 소급 실행
#   하지 않겠다는 뜻입니다. True면 밀린 기간만큼 한꺼번에 실행됩니다.
# - `tags`: UI 목록에서 DAG를 검색·분류하는 라벨입니다.
# ───────────────────────────────────────────────────────────────────
def lab02_hello_pipeline_explained():

    @task
    def download_data() -> str:
        import io
        import urllib.request
        import zipfile
        from pathlib import Path

        Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(DATA_URL) as resp:
            zipfile.ZipFile(io.BytesIO(resp.read())).extractall(DATA_DIR)
        return f"{DATA_DIR}/ml-100k/u.data"

    # ── 🔬 코드 해설: download_data ─────────────────────────────────
    # - `@task`: 이 함수 하나가 그래프의 노드 하나(Task)가 됩니다.
    # - import가 함수 안에 있는 이유: Task 코드는 "실행될 때만" 필요
    #   합니다. 상단 해설처럼, 파일 파싱 단계를 가볍게 유지하는 것이
    #   Airflow의 권장 습관입니다.
    # - `return`된 문자열(데이터 경로)은 XCom이라는 저장소에 기록되어
    #   다음 Task의 인자로 자동 전달됩니다. 큰 데이터 자체가 아니라
    #   "경로"처럼 작은 값을 넘기는 것이 원칙입니다.
    # ────────────────────────────────────────────────────────────────

    @task
    def preprocess(ratings_path: str) -> dict:
        from collections import defaultdict

        rows = []
        with open(ratings_path) as f:
            for line in f:
                user, item, _rating, ts = line.split("\t")
                rows.append((int(user), int(item), int(ts)))
        rows.sort(key=lambda r: (r[0], r[2]))  # 사용자별 timestamp 순 정렬

        seqs = defaultdict(list)
        for user, item, _ts in rows:
            seqs[user].append(item)

        lens = [len(s) for s in seqs.values()]
        return {
            "n_users": len(seqs),
            "n_events": len(rows),
            "min_len": min(lens),
            "max_len": max(lens),
        }

    # ── 🔬 코드 해설: preprocess ────────────────────────────────────
    # - 인자 `ratings_path`에는 앞 Task의 반환값이 들어옵니다. 함수
    #   호출처럼 보이지만, 실제로는 XCom을 통해 "다른 프로세스에서
    #   실행된 Task의 결과"를 받는 것입니다.
    # - timestamp로 정렬해 사용자 시퀀스를 만드는 로직은 5주차 SASRec
    #   전처리와 동일한 아이디어입니다. 이번 주차는 이 익숙한 코드를
    #   "자동 실행되는 단위(Task)"로 옮기는 것이 핵심입니다.
    # - 반환값이 dict여도 됩니다. XCom은 JSON으로 직렬화 가능한 작은
    #   값을 전달하는 용도이기 때문입니다.
    # ────────────────────────────────────────────────────────────────

    @task
    def report(stats: dict):
        print(f"사용자 수      : {stats['n_users']}")
        print(f"행동(평점) 수  : {stats['n_events']}")
        print(f"시퀀스 길이    : 최소 {stats['min_len']} ~ 최대 {stats['max_len']}")

    # ── 🔬 코드 해설: report ────────────────────────────────────────
    # - `print` 출력은 사라지지 않고 해당 Task의 "로그"로 저장됩니다.
    #   UI에서 Task를 클릭 → Logs 탭에서 언제든 다시 볼 수 있습니다.
    #   "기록이 휘발되는 노트북"과의 첫 번째 차이가 이것입니다.
    # ────────────────────────────────────────────────────────────────

    report(preprocess(download_data()))

    # ── 🔬 코드 해설: 의존 관계 연결 ────────────────────────────────
    # - `report(preprocess(download_data()))` 한 줄이 곧 의존 관계
    #   선언입니다: download_data → preprocess → report.
    #   TaskFlow API에서는 "반환값을 인자로 쓰는 관계"가 그대로
    #   그래프의 화살표가 됩니다.
    # - 여기서 함수가 즉시 실행되는 것이 아닙니다. 이 호출은 "설계도
    #   (DAG)"를 그릴 뿐이고, 실제 실행은 Scheduler가 트리거 시점에
    #   Task 단위로 진행합니다.
    # ────────────────────────────────────────────────────────────────


lab02_hello_pipeline_explained()

# ── 🔬 코드 해설: DAG 인스턴스화 ────────────────────────────────────
# - 마지막 줄의 호출이 있어야 Scheduler가 이 파일에서 DAG를 발견합니다.
#   "@dag가 붙은 함수를 모듈 수준에서 한 번 호출"이 TaskFlow의 규칙입니다.
# ────────────────────────────────────────────────────────────────────
