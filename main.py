import logging
from fastapi import FastAPI
from auth.router import router as auth_router
from users.router import router as user_router
from form_admin.router import router as form_router
from tasks.router import router as task_router
from models.user import Base
from database import engine
from config import config

Base.metadata.create_all(bind=engine)


app = FastAPI(title=config().app_name)
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
logger.info("Application starting...")
