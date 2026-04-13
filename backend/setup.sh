#!/bin/bash

# 로컬에서의 테스트 용도

echo "FDS Backend 가상환경 구축 시작"

apt install python3.12-venv

if [ -d ".venv" ]; then
    echo "기존 가상환경(.venv) 삭제 중..."
    rm -rf .venv
fi

echo "가상환경 생성 중..."
python3 -m venv .venv

echo "필수 패키지 설치 중..."
source .venv/bin/activate

pip install --upgrade pip
pip install fastapi uvicorn requests pydantic redis

# Docker가 설치되어 있다면 Redis 컨테이너를 실행합니다.
if command -v docker &> /dev/null
then
    echo "Redis 컨테이너 실행 중 (stockguard-redis)..."
    docker run -d --name stockguard-redis -p 6379:6379 redis:alpine || echo "Redis가 이미 실행 중이거나 Docker 실행에 실패했습니다."
else
    echo "⚠️ Docker가 설치되어 있지 않습니다. 로컬에 Redis 서버가 실행 중이어야 테스트가 가능합니다."
fi

echo "Setup 완료"

