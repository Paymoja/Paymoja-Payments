from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Header
from dependencies.auth_depencies import verify_auth_details
from dependencies.db import get_db

router = APIRouter(
    prefix='/api/ug/airtel',
    tags=['Airtel Uganda Payments'],
    responses={404: {"description": "oops can't help you with that!"}},
)






