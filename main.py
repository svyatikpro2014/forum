from fastapi import FastAPI
from database import setup_database
import uvicorn
from routers.endpoints import router as posts_router


app = FastAPI()


app.include_router(posts_router)

@app.on_event("startup")
async def startup():
    await setup_database()

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
