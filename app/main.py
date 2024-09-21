from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine
from .routers import post_router, user_router, refresh_token_router
from fastapi.staticfiles import StaticFiles

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router.router)
app.include_router(refresh_token_router.router)
app.include_router(post_router.router)

app.mount("/media", StaticFiles(directory="app/media"), name="media")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Navigate to /docs to see the API documentation."}

