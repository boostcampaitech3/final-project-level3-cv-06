import os
from PIL import Image
from fastapi import FastAPI, UploadFile, File, APIRouter, Depends
from fastapi.param_functions import Depends
from uuid import UUID, uuid4
from typing import List, Union, Optional, Dict, Any
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from app.ml.model_inference import img_inference
from app.utils.token import AuthHandler
from app.dao.image_dao import save_image
from app.service.image_service import check_path, get_img_info
from app.database.conn import db
from app.common.const import IMAGE_BASE as BASE
from app.service.auth_service import is_id_exist, check_user_history


# from fastapi_pagination import Page, paginate, add_pagination

router = APIRouter(prefix='/img')

@router.post('/order', description="get img_file from frontend")
async def make_inference(file: UploadFile = File(...), id=Depends(AuthHandler().auth_wrapper), session: Session=Depends(db.session)):
    if not await is_id_exist(id):
        return JSONResponse(status_code=400, content=dict(msg="NO USER EXIST"))
    
    img = Image.open(file.file).convert('RGB')
    if not check_path(BASE):
        os.mkdir(BASE)
    
    img_path = f"{BASE}/{str(uuid4())}.jpg"
    
    save_image(img_path, img, id, session)

    result = img_inference(img_path, session)
    
    return result


@router.get('/history', description="get all user's inference informations")
async def inference_history(id=Depends(AuthHandler().auth_wrapper), session: Session=Depends(db.session)):
    if not await is_id_exist(id):
        return JSONResponse(status_code=400, content=dict(msg="NO USER EXIST"))
    if not check_user_history(id):
        return JSONResponse(status_code=400, content=dict(msg="NO HISTORY"))
    inference_infos = get_img_info(id, session)

    return JSONResponse(status_code=200, content=inference_infos)