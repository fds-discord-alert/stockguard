import os
import time
import redis
from models.schemas import Transaction

# Redis 연결 설정 (환경변수 REDIS_HOST가 없으면 localhost 사용)
try:
    redis_host = os.getenv("REDIS_HOST", "localhost")
    # decode_responses=True를 설정하여 문자열로 데이터를 주고받습니다.
    r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
    # 연결 테스트
    r.ping()
except (redis.exceptions.ConnectionError, Exception):
    r = None
    print(f"⚠️ Redis({redis_host}) 연결 실패: Velocity Check가 비활성화됩니다.")

# 설정값: 1초 이내에 3번 이상 거래 시 탐지
TIME_WINDOW = 1  
MAX_TRANSACTIONS = 3

def detect_fraud(tx: Transaction) -> tuple[bool, str]:
    """
    거래 데이터를 분석하여 이상 여부를 판별합니다.
    1. 고액 거래 탐지 (Amount > 1,000,000,000)
    2. 해외 접속 탐지 (Non-Korea)
    3. Redis 기반 단시간 반복 거래 탐지 (Velocity Check)
    """
    
    # 1. 고액 거래 검사 (10억 초과)
    if tx.amount > 1000000000:
        return True, f"Suspicious activity: Extremely large amount ({tx.amount:,} KRW)."

    # 2. 해외 접속 (Korea가 아닌 경우)
    if tx.location != "Korea":
        return True, f"Suspicious activity: Connection from abroad ({tx.location})."

    # 3. Redis 기반 Velocity Check (반복 거래 탐지)
    if r is not None:
        user_key = f"user_tx:{tx.user_id}"
        current_time = time.time()
        
        try:
            # 윈도우 밖의 오래된 데이터 제거 (Sliding Window)
            r.zremrangebyscore(user_key, 0, current_time - TIME_WINDOW)
            
            # 새로운 거래 내역 추가 (타임스탬프를 스코어로 저장)
            r.zadd(user_key, {str(current_time): current_time})
            
            # 현재 윈도우 내의 거래 횟수 확인
            tx_count = r.zcard(user_key)
            
            # 데이터 만료 시간 설정 (메모리 관리용)
            r.expire(user_key, TIME_WINDOW)
            
            if tx_count >= MAX_TRANSACTIONS:
                return True, f"Suspicious activity: Multiple transactions ({tx_count} times) within {TIME_WINDOW}s."
        except Exception as e:
            print(f"Redis Operation Error: {e}")

    return False, ""
