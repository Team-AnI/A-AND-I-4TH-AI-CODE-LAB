"""실습 1: 첫 Airflow DAG (따라하기)

MovieLens 데이터를 내려받아 사용자 시퀀스 통계를 출력하는,
download → preprocess → report 세 Task짜리 가장 작은 파이프라인입니다.
이 파일을 dags/ 폴더에 넣고, Airflow UI에서 `lab01_hello_pipeline`을
수동 트리거한 뒤 그래프 뷰와 Task 로그를 확인하세요.
"""
from datetime import datetime

from airflow.decorators import dag, task

DATA_URL = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
DATA_DIR = "/opt/airflow/data"


@dag(
    schedule=None,  # 실습에서는 UI에서 수동 트리거
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["recsys", "lab01"],
)
def lab01_hello_pipeline():

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

    @task
    def report(stats: dict):
        print(f"사용자 수      : {stats['n_users']}")
        print(f"행동(평점) 수  : {stats['n_events']}")
        print(f"시퀀스 길이    : 최소 {stats['min_len']} ~ 최대 {stats['max_len']}")

    report(preprocess(download_data()))


lab01_hello_pipeline()
