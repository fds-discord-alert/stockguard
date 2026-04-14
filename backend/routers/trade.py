from fastapi import APIRouter
from models.schemas import Transaction
from services.fds_logic import detect_fraud
from services.discord_bot import send_alert

router = APIRouter()

@router.post("/trade")
async def process_trade(tx: Transaction):
    """
    실제 거래 데이터를 POST 방식으로 전달받아 이상 여부를 검사합니다.
    """
    is_fraud, reason, severity, color = detect_fraud(tx)
    
    if is_fraud:
        # 이상 거래 탐지 시 상세 정보와 함께 Discord 알림 전송
        title = "🚨 StockGuard FDS 이상 거래 감지"
        description = (
            f"**사용자 ID:** `{tx.user_id}`\n"
            f"**종목명:** {tx.stock_name}\n"
            f"**거래 금액:** {tx.amount:,}원\n"
            f"**접속 정보:** {tx.location}\n"
            f"**탐지 사유:** {reason}"
        )
        
        send_alert(title, description, severity, color)
        
        return {"status": "BLOCKED", "reason": reason}

    # 정상 거래일 경우 승인 응답 반환
    return {"status": "APPROVED"}