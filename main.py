import sys
import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from auth.router import router as auth_router
from users.router import router as user_router
from form_admin.router import router as form_router
from tasks.router import router as task_router
from models.model import Base
from database import engine
from config import config
from models.user import User
from models.auth_token import AuthToken
from models.form import Form

Base.metadata.create_all(bind=engine)

app = FastAPI(title=config().app_name)

origins = [
    "http://5.45.125.9",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, tags=["user"])
app.include_router(form_router, prefix="/forms", tags=["form_admin"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler()  # Log messages to the console
    ]
)

# Log a message
logger = logging.getLogger(__name__)

if "--db_seed" in sys.argv:
    logger.info("Database seeding...")
    from seeders.db_seeder import seed

    seed()
else:
    logger.info("Application starting...")
