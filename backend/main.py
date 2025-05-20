from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import methods

app = FastAPI()

# CORS pour autoriser l'accès du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou spécifie ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(methods.router)
