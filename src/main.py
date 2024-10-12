from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api import information, history, business_client, company_vision_values, business_area, inquiry

app = FastAPI()

# 모든 도메인에 대해 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ["http://example.com"] 처럼 특정 도메인만 허용 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 제공 경로 설정
app.mount("/logos", StaticFiles(directory="logos"), name="logos")

app.include_router(information.router)
app.include_router(history.router)
app.include_router(business_client.router)
app.include_router(company_vision_values.router)
app.include_router(business_area.router)
app.include_router(inquiry.router)

@app.get("/")
def checking():
    return {"connect" : "success"}
