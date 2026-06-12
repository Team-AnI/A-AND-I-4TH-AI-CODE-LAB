# 실습용 Airflow 이미지 — torch(CPU 전용)·wandb를 미리 설치합니다.
# 컨테이너 시작 시 pip 설치(_PIP_ADDITIONAL_REQUIREMENTS)를 쓰지 않는 이유:
# 매 시작마다 재설치되고, 설치가 끝나기 전 헬스체크가 실패할 수 있기 때문입니다.
FROM apache/airflow:3.2.2

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir wandb
