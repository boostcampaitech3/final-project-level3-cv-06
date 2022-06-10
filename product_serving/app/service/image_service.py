import os

from app.dao.image_dao import get_img_info_dao


def check_path(cur_path):
    if os.path.exists(cur_path):
        return True
    
    return False

def get_img_info(id, session):
    inference_infos = get_img_info_dao(id, session)
    
    inference_info_list = [{
        "user_id": info[0],
        "image_path": info[1],
        "xmin": info[2],
        "ymin": info[3],
        "xmax": info[4],
        "ymax": info[5],
        "trouble_type": info[6],
        'image_updated_at': info[7].strftime("%Y.%m.%d %H:%m"),
    }for info in inference_infos]
    
    return inference_info_list

