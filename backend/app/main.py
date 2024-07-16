import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()
from app.routes.api import router
app.include_router(router, prefix="/api", tags=[""])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
    allow_credentials=True,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


from app.database.redis_base import redis_client


@app.on_event("startup")
async def startup_events():
    try:
        redis_client.init_connection()
    except Exception as e:
        print(str(e))


@app.on_event("shutdown")
async def shutdown_events():
    try:
        await redis_client.close_connection()
        print("Shutdown connection to Redis")
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=10086)
