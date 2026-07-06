from fastapi import FastAPI
from database import setup_database
import uvicorn
from routers.endpoints import router as posts_router
from routers.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(posts_router)
app.include_router(auth_router)

@app.on_event("startup")
async def startup():
    await setup_database()

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
