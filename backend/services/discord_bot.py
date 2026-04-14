import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경변수에서 웹후크 URL 가져오기
WEBHOOK_URL = os.getenv("webhook_url")

def send_alert(title: str, description: str, severity: str, color: int):
    """
    팀원이 구현한 Discord Embed 알림 전송 함수입니다.
    디버깅을 위한 로그가 추가되었습니다.
    """
    print(f"\n📡 [Discord] 알림 전송 시도 중...")
    print(f"   - 제목: {title}")
    print(f"   - 심각도: {severity}")

    if not WEBHOOK_URL or "YOUR_DISCORD_WEBHOOK_URL" in WEBHOOK_URL:
        print("⚠️ [Discord] 유효한 WEBHOOK_URL이 설정되지 않았습니다. (.env 파일을 확인하세요)")
        return

    try:
        payload = {
            "embeds": [
                {
                    "title": title,
                    "description": description,
                    "color": color,
                    "fields": [
                        {"name": "심각도", "value": severity, "inline": True},
                        {"name": "시각", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": True}
                    ],
                    "footer": {"text": "📊 StockGuard Monitoring"}
                }
            ]
        }
        
        # 전송 전 로그
        print(f"   - 전송 URL: {WEBHOOK_URL[:30]}...") 
        
        response = requests.post(WEBHOOK_URL, json=payload)
        
        if response.status_code == 204:
            print(f"✅ [Discord] 알림 전송 성공!")
        else:
            print(f"❌ [Discord] 전송 실패 (Status: {response.status_code}): {response.text}")

    except Exception as e:
        print(f"❌ [Discord] 알림 전송 중 예외 발생: {e}")
