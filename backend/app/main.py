from fastapi import FastAPI

from backend.app.routes.auth import router as auth_router
from backend.app.routes.projects import router as projects_router
from backend.app.routes.documents import router as documents_router
from backend.app.routes.follows import router as follows_router
from backend.app.routes.files import router as files_router
from backend.app.routes.comments import router as comments_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(follows_router)
app.include_router(projects_router)
app.include_router(documents_router)
app.include_router(files_router)
app.include_router(comments_router)


