import os
import time
import redis
import requests
from models.schemas import Transaction

# Redis 연결 설정
try:
    redis_host = os.getenv("REDIS_HOST", "localhost")
    r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
    r.ping()
except (redis.exceptions.ConnectionError, Exception):
    r = None
    print(f"⚠️ Redis({redis_host}) 연결 실패: Velocity Check가 비활성화됩니다.")

# 설정값
TIME_WINDOW = 1  
MAX_TRANSACTIONS = 3

def check_foreign_ip(ip: str) -> bool:
    """
    IP 주소를 기반으로 해외 접속 여부를 판단합니다. (팀원 구현 로직)
    """
    if not ip or ip == "localhost" or ip.startswith("127."):
        return False

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        country = data.get("country", "")
        # 한국이 아니면 해외로 간주
        return country != "South Korea"
    except Exception as e:
        print(f"⚠️ IP 조회 실패 ({ip}): {e}")
        return False

def detect_fraud(tx: Transaction) -> tuple[bool, str, str, int]:
    """
    거래 데이터를 분석하여 이상 여부를 판별합니다.
    반환값: (이상여부, 사유, 심각도, 색상)
    """
    
    # 1. 고액 거래 탐지 (10억 초과)
    if tx.amount > 1000000000:
        return True, f"Extremely large amount ({tx.amount:,} KRW).", "CRITICAL", 16711680

    # 2. 해외 IP 접속 탐지 (팀원 로직 기반)
    # location 필드에 IP 주소가 들어온다고 가정하거나, 팀원 로직을 활용합니다.
    if check_foreign_ip(tx.location):
        return True, f"Connection from abroad ({tx.location}).", "HIGH", 255

    # 3. Redis 기반 Velocity Check (반복 거래 탐지)
    if r is not None:
        user_key = f"user_tx:{tx.user_id}"
        current_time = time.time()
        
        try:
            # 윈도우 밖의 오래된 데이터 제거 (Sliding Window)
            r.zremrangebyscore(user_key, 0, current_time - TIME_WINDOW)
            
            # 새로운 거래 내역 추가
            r.zadd(user_key, {str(current_time): current_time})
            
            # 현재 윈도우 내의 거래 횟수 확인
            tx_count = r.zcard(user_key)
            r.expire(user_key, TIME_WINDOW)
            
            if tx_count >= MAX_TRANSACTIONS:
                return True, f"Multiple transactions ({tx_count} times) within {TIME_WINDOW}s.", "WARNING", 16753920
        except Exception as e:
            print(f"Redis Operation Error: {e}")

    return False, "", "", 0
