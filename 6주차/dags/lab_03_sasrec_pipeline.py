"""실습 3: SASRec 학습 파이프라인 (확장 — Airflow + WandB)

5주차 lab_03에서 구현한 SASRec 학습 루프를 Airflow DAG로 감싸고,
매 epoch의 loss·HR@10·NDCG@10을 WandB로 기록합니다.

    download_data → preprocess → train_and_evaluate (WandB 기록)

사전 조건: WANDB_API_KEY 환경변수가 컨테이너에 주입되어 있어야 합니다.
(주입 방법은 6주차 README의 "환경 구축" 참고 — 키를 코드에 적지 않습니다.)

[개념 복기 및 이론 점검 — 실행 전에 스스로 답해 보세요]
- 5주차에서는 이 학습을 노트북 셀로 실행했습니다. Task로 옮기면
  무엇이 달라질까요? (재시도, 로그, 의존 관계)
- Airflow와 WandB의 역할은 어떻게 나뉠까요? (실행 vs 관측)
- leave-one-out 평가에서 valid와 test를 나누는 이유는 무엇일까요?
"""
from datetime import datetime

from airflow.decorators import dag, task

# ── 데이터셋 설정 ───────────────────────────────────────────────────
# 기본: MovieLens 100K. 1M으로 확장하려면 아래 주석을 교체합니다.
DATA_URL = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
# DATA_URL = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"

DATA_DIR = "/opt/airflow/data"

# WandB run 비교 실습: hidden·epochs 등을 바꿔 재실행한 뒤
# 대시보드에서 두 run을 겹쳐 비교해 보세요.
CONFIG = {
    "max_len": 50,
    "hidden": 64,
    "blocks": 2,
    "heads": 2,
    "dropout": 0.2,
    "epochs": 10,
    "batch_size": 128,
    "lr": 1e-3,
}


@dag(
    schedule=None,  # 실습에서는 UI에서 수동 트리거
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["recsys", "sasrec", "lab03"],
)
def lab03_sasrec_pipeline():

    @task
    def download_data() -> str:
        import io
        import urllib.request
        import zipfile
        from pathlib import Path

        Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(DATA_URL) as resp:
            zipfile.ZipFile(io.BytesIO(resp.read())).extractall(DATA_DIR)
        return DATA_DIR

    @task
    def preprocess(data_dir: str) -> str:
        from collections import defaultdict
        from pathlib import Path

        import torch

        # 100K와 1M은 파일명·구분자가 다릅니다. DATA_URL 기준으로 결정.
        name = DATA_URL.split("/")[-1].removesuffix(".zip")
        if name == "ml-100k":
            path, sep = Path(data_dir) / name / "u.data", "\t"
        else:
            path, sep = Path(data_dir) / name / "ratings.dat", "::"

        rows = []
        for line in path.read_text().splitlines():
            user, item, _rating, ts = line.split(sep)
            rows.append((int(user), int(item), int(ts)))
        rows.sort(key=lambda r: (r[0], r[2]))  # 사용자별 timestamp 순 정렬

        seqs = defaultdict(list)
        for user, item, _ts in rows:
            seqs[user].append(item)
        # leave-one-out: 마지막 아이템=test, 그 앞=valid, 나머지=train
        user_seqs = [s for s in seqs.values() if len(s) >= 4]
        n_items = max(i for s in user_seqs for i in s)

        max_len = CONFIG["max_len"]
        inputs, targets = [], []
        for s in user_seqs:
            train_part = s[:-2]
            window = train_part[-(max_len + 1):]
            inp, tgt = window[:-1], window[1:]
            pad = max_len - len(inp)
            inputs.append([0] * pad + inp)
            targets.append([0] * pad + tgt)

        out = Path(data_dir) / "sasrec_train.pt"
        torch.save(
            {
                "inputs": torch.tensor(inputs),
                "targets": torch.tensor(targets),
                "user_seqs": user_seqs,
                "n_items": n_items,
            },
            out,
        )
        return str(out)

    @task
    def train_and_evaluate(train_path: str):
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        from torch.utils.data import DataLoader, TensorDataset

        import wandb

        torch.manual_seed(42)
        device = "cuda" if torch.cuda.is_available() else "cpu"

        data = torch.load(train_path)
        inputs, targets = data["inputs"], data["targets"]
        user_seqs, n_items = data["user_seqs"], data["n_items"]
        max_len = CONFIG["max_len"]
        vocab = n_items + 1

        # ▼ 5주차 lab_03에서 구현한 SASRec — 구조 그대로 재사용
        class SASRec(nn.Module):
            def __init__(self):
                super().__init__()
                self.item_emb = nn.Embedding(vocab, CONFIG["hidden"], padding_idx=0)
                self.pos_emb = nn.Embedding(max_len, CONFIG["hidden"])
                layer = nn.TransformerEncoderLayer(
                    CONFIG["hidden"],
                    CONFIG["heads"],
                    dim_feedforward=CONFIG["hidden"] * 2,
                    dropout=CONFIG["dropout"],
                    batch_first=True,
                )
                self.encoder = nn.TransformerEncoder(layer, CONFIG["blocks"])

            def forward(self, seq):
                L = seq.size(1)
                pos = torch.arange(L, device=seq.device).unsqueeze(0)
                x = self.item_emb(seq) + self.pos_emb(pos)
                causal = torch.triu(
                    torch.full((L, L), float("-inf"), device=seq.device), diagonal=1
                )
                h = self.encoder(x, mask=causal)
                return h @ self.item_emb.weight.T

        def pad_batch(prefixes):
            batch = []
            for p in prefixes:
                w = p[-max_len:]
                batch.append([0] * (max_len - len(w)) + w)
            return torch.tensor(batch, device=device)

        @torch.no_grad()
        def evaluate(offset):
            """leave-one-out 평가. offset=2 → valid, offset=1 → test."""
            model.eval()
            prefixes = [s[:-offset] for s in user_seqs]
            target = torch.tensor([s[-offset] for s in user_seqs], device=device)
            scores = model(pad_batch(prefixes))[:, -1]  # (n_users, vocab)
            scores[:, 0] = -float("inf")
            for row, p in enumerate(prefixes):  # 이미 본 아이템 제외
                scores[row, p] = -float("inf")
            tgt_score = scores.gather(1, target.unsqueeze(1))
            rank = (scores > tgt_score).sum(dim=1) + 1
            hr = (rank <= 10).float().mean().item()
            ndcg = (
                torch.where(
                    rank <= 10,
                    1.0 / torch.log2(rank.float() + 1),
                    torch.zeros_like(rank, dtype=torch.float),
                )
                .mean()
                .item()
            )
            return hr, ndcg

        model = SASRec().to(device)
        opt = torch.optim.Adam(model.parameters(), lr=CONFIG["lr"])
        dl = DataLoader(
            TensorDataset(inputs, targets),
            batch_size=CONFIG["batch_size"],
            shuffle=True,
        )

        run = wandb.init(project="club-airflow-sasrec", config=CONFIG)
        for epoch in range(1, CONFIG["epochs"] + 1):
            model.train()
            total = 0.0
            for xb, yb in dl:
                xb, yb = xb.to(device), yb.to(device)
                opt.zero_grad()
                loss = F.cross_entropy(
                    model(xb).reshape(-1, vocab), yb.reshape(-1), ignore_index=0
                )
                loss.backward()
                opt.step()
                total += loss.item()
            hr, ndcg = evaluate(offset=2)
            run.log({"loss": total / len(dl), "HR@10": hr, "NDCG@10": ndcg})
            print(
                f"epoch {epoch}  loss {total / len(dl):.4f}"
                f"  valid HR@10 {hr:.4f}  NDCG@10 {ndcg:.4f}"
            )

        hr, ndcg = evaluate(offset=1)
        run.summary["test_HR@10"] = hr
        run.summary["test_NDCG@10"] = ndcg
        run.finish()
        print(f"최종 테스트  HR@10 {hr:.4f}  NDCG@10 {ndcg:.4f}")

    train_and_evaluate(preprocess(download_data()))


lab03_sasrec_pipeline()
