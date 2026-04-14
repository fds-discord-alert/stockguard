import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

webhook_url = os.getenv("webhook_url")


def send_alert(title, description, severity, color):
    try:
        response = requests.post(webhook_url, json={
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
        })

        if response.status_code != 204:
            print("❌ Discord 전송 실패:", response.text)

    except Exception as e:
        print("❌ 알림 전송 오류:", e)


def detect_abnormal_trade(order_speed, order_time, is_foreign_ip):

    # 🚨 1️⃣ 비정상 주문 속도
    if order_speed > 100:
        send_alert(
            "🚨 비정상 주문 속도 감지",
            f"초당 주문 수가 비정상적으로 증가했습니다.\n\n📈 주문 속도: {order_speed}건/sec",
            "CRITICAL",
            16711680  # 빨강
        )
        

    # 🌙 2️⃣ 이상 시간 거래
    hour = order_time.hour
    if 2 <= hour <= 6:
        send_alert(
            "🌙 이상 시간 거래 감지",
            f"비정상 시간대에 거래가 발생했습니다.\n\n⏰ 현재 시간: {hour}시",
            "WARNING",
            16753920  # 주황
        )
        

    # 🌍 3️⃣ 해외 IP 접속
    if is_foreign_ip:
        send_alert(
            "🌍 해외 IP 접속 감지",
            "해외에서 거래가 발생했습니다.\n\n🔎 추가 확인이 필요합니다.",
            "HIGH",
            255  # 파랑
        )
        


# 데이터 처리
def calculate_order_speed(order):
    return order.get("speed", 0)


def check_foreign_ip(order):
    return order.get("is_foreign", False)


def process_order(order):
    order_speed = calculate_order_speed(order)
    is_foreign = check_foreign_ip(order)
    current_time = datetime.now()

    detect_abnormal_trade(order_speed, current_time, is_foreign)


# 테스트
if __name__ == "__main__":
    order = {
        "speed": 120,
        "is_foreign": True
    }

    process_order(order)