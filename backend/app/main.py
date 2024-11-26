from fastapi import FastAPI
from .routes.auth import router as auth_router
from .routes.projects import router as projects_router
from .routes.documents import router as documents_router
from .routes.follows import router as follows_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(follows_router)
app.include_router(projects_router)
app.include_router(documents_router)


