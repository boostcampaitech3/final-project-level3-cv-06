import os
import cv2
import mmcv
import json

from PIL import Image
from app.dao.image_dao import save_trouble_info
from app.common.const import MMCONFIG as CONF_BASE, MODEL_CONF_DIR, MODEL_DIR
from pycocotools.coco import COCO
from mmdet.models import build_detector
from mmdet.apis import single_gpu_test
from mmdet.datasets import (build_dataloader, build_dataset,
                            replace_ImageToTensor)

from sahi.model import MmdetDetectionModel, Yolov5DetectionModel
from sahi.predict import get_prediction, get_sliced_prediction, predict


def get_trouble_type_bbox(result):
    # trouble category와 bbox 정보 제공

    raw_infos = result.object_prediction_list
    trouble_info = []
    for info in raw_infos:
        temp = {}
        temp['trouble_type'] = info.category.__dict__['id'] + 1
        temp['bbox'] = [info.bbox.__dict__['minx'], 
                        info.bbox.__dict__['miny'],
                        info.bbox.__dict__['maxx'],
                        info.bbox.__dict__['maxy']]
        trouble_info.append(temp)

    return trouble_info


def pred_img_viz(img_path, trouble_info):
    cate_col = {1: (192, 0, 128), 2: (192, 128, 64), 3: (0, 128, 64)}
    origin_img = cv2.imread(img_path)
    
    for tr in trouble_info:
        rect = tr['bbox']
        
        cv2.rectangle(origin_img, (rect[0], rect[1]), (rect[2], rect[3]), color=cate_col[tr['trouble_type']], thickness=1)
        cv2.putText(origin_img, f"type{tr['trouble_type']}", (rect[0], rect[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cate_col[tr['trouble_type']], thickness=1)

    return origin_img

def count_trouble_type(trouble_info):
    troub = dict(type1=0, type2=0, type3=0)
    
    for t in trouble_info:
        if t['trouble_type'] == 1:
            troub['type1'] += 1
        elif t['trouble_type'] == 2:
            troub['type2'] += 1
        else:
            troub['type3'] += 1
    
    return troub

def img_inference(img_path, session):
    mm_conf_path = MODEL_CONF_DIR
    mm_model_path = MODEL_DIR
    
    mmdet_model = MmdetDetectionModel(
        model_path=mm_model_path,
        config_path=mm_conf_path,
        confidence_threshold=0.35,
        device="cuda:0",
    )

    result = get_sliced_prediction(
        img_path,
        mmdet_model,
        slice_height = 512,
        slice_width = 512,
        overlap_height_ratio = 0.4,
        overlap_width_ratio = 0.4,
    )

    trouble_info = get_trouble_type_bbox(result)
    save_trouble_info(img_path, trouble_info, session) # inference table에 trouble 정보, bbox 정보 저장
    
    trouble_count = count_trouble_type(trouble_info)
    pred_img = pred_img_viz(img_path, trouble_info)
    save_predicted_img_dir = f'/opt/ml/input/fastapi_serving/app/predicted_img/{img_path[45:]}'
    
    cv2.imwrite(save_predicted_img_dir, pred_img)

    return {"img_path": save_predicted_img_dir, 
            "type1": trouble_count["type1"],
            "type2": trouble_count["type2"],
            "type3": trouble_count["type3"],
            }
