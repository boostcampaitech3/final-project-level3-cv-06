from PIL import Image as im
from app.database.models import User, Image, Inference
from fastapi import HTTPException


def save_image(img_path, img, id, session):
    re_img = img.resize((1024, 1024))
    re_img.save(img_path)

    Image.create(
        session, auto_commit=True,
        image_path=img_path,
        user_id = id,
    )


# 이미지에 대한 inference 정보를 inference table에 저장
def save_trouble_info(img_path, trouble_info, session):
    image = Image.get(image_path=img_path)

    for tr in trouble_info:
        Inference.create(
            session, auto_commit=True,
            trouble_type=tr['trouble_type'],
            xmin = tr['bbox'][0],
            ymin = tr['bbox'][1],
            xmax = tr['bbox'][2],
            ymax = tr['bbox'][3],
            image_id = image.id
        )

def get_img_info_dao(id, session):
    try:
        user = User.get(id=id)
        data = session.query(
            User.user_id,
            Image.image_path,
            Inference.xmin,
            Inference.ymin,
            Inference.xmax,
            Inference.ymax,
            Inference.trouble_type,
            Image.updated_at
            )\
            .join(User, User.id == Image.user_id) \
            .join(Inference, Inference.image_id == Image.id) \
            .filter(User.id==user.id)
    except:
        raise HTTPException(status_code=400, detail="CANNOT FIND DATA")

    return data