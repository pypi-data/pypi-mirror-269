"""app.py"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import database
from models import environment as m_environment
import endpoints.compile_req
import endpoints.generate_img
import endpoints.pip_compile

app = FastAPI()
# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
# Database setup
db_con = database.Database()
m_environment.Base.metadata.create_all(bind=db_con.create_database_engine())

# Routers
app.include_router(endpoints.compile_req.router)
app.include_router(endpoints.generate_img.router)
app.include_router(endpoints.pip_compile.router)
