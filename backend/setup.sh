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

pip install fastapi uvicorn requests pydantic

echo "Setup 완료"

