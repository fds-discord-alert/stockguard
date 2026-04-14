import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

webhook_url = os.getenv("webhook_url")


# =========================
# 🚨 Discord 알림
# =========================
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


# =========================
# 🌍 IP → 국가 조회
# =========================
def check_foreign_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()

        country = data.get("country", "")

        # 한국 아니면 해외
        return country != "South Korea"

    except Exception as e:
        print("IP 조회 실패:", e)
        return False


# =========================
# 🚨 이상 거래 탐지
# =========================
def detect_abnormal_trade(order_speed, order_time, is_foreign_ip):

    # 1️⃣ 속도 이상
    if order_speed > 100:
        send_alert(
            "🚨 비정상 주문 속도 감지",
            f"📈 주문 속도: {order_speed}건/sec",
            "CRITICAL",
            16711680
        )

    # 2️⃣ 이상 시간
    if 2 <= order_time.hour <= 6:
        send_alert(
            "🌙 이상 시간 거래 감지",
            f"⏰ 현재 시간: {order_time.hour}시",
            "WARNING",
            16753920
        )

    # 3️⃣ 해외 IP
    if is_foreign_ip:
        send_alert(
            "🌍 해외 IP 접속 감지",
            "해외에서 거래가 발생했습니다.",
            "HIGH",
            255
        )


# =========================
# 📦 데이터 처리
# =========================
def calculate_order_speed(order):
    return order.get("speed", 0)


def extract_ip(order):
    return order.get("ip", None)


# =========================
# 🔄 전체 흐름
# =========================
def process_order(order, test_time=None):

    order_speed = calculate_order_speed(order)

    # 시간 처리 (테스트 가능)
    current_time = test_time if test_time else datetime.now()

    # IP → foreign 여부 판단
    ip = extract_ip(order)
    is_foreign = False

    if ip:
        is_foreign = check_foreign_ip(ip)

    detect_abnormal_trade(order_speed, current_time, is_foreign)


# =========================
# 🧪 테스트 코드
# =========================
if __name__ == "__main__":

    # 테스트용 주문 데이터
    order = {
        "speed": 120,
        "ip": "8.8.8.8"   # 👉 미국 IP (해외 테스트용)
    }

    # 👉 시간도 강제 지정 가능
    from datetime import datetime
    test_time = datetime(2026, 4, 13, 3)  # 새벽 3시

    process_order(order, test_time)