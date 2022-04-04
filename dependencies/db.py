from fastapi import HTTPException
from utils.database import SessionLocal
import structlog

struct_logger = structlog.get_logger(__name__)


def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception as e:

        struct_logger.error(event="create database session", message="Failed to connect to database",
                            error=str(type(e)))
        raise HTTPException(status_code=404, detail="Could not connect to database : {}".format(e))
    finally:
        db.close()
