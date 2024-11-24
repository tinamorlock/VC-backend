from fastapi import FastAPI
from .routes.auth import router as auth_router
from .routes.projects import router as projects_router

app = FastAPI()

app.include_router(auth_router) # for user reg and login
app.include_router(projects_router) # for project setup


