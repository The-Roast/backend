from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from theroast.config import server_config
from theroast.app import schemas

router = APIRouter()

@router.get("/", response_model=)