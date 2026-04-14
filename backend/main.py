from fastapi import FastAPI
from routers.trade import router as trade_router

app = FastAPI(title="StockGuard FDS API")

@app.get("/health")
async def health_check():
    """
    Kubernetes Health Check를 위한 엔드포인트
    """
    return {"status": "ok"}

# trade 라우터를 등록합니다.
app.include_router(trade_router)

if __name__ == "__main__":
    import uvicorn
    # 로컬 개발 테스트용 실행 구성
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)