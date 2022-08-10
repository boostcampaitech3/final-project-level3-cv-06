import re
import bcrypt
from app.utils.token import AuthHandler
from app.database.models import User, Image
from app.database.schema import UserRegister, Login

authhandler = AuthHandler()


async def is_username_exist(user_id: str):
    get_user_id = User.get(user_id=user_id)
    if get_user_id:
        return True
    return False


async def is_id_exist(id: int):
    get_id = User.get(id=id)
    if get_id:
        return True
    return False

def create_user(info: UserRegister, session):
    hash_pw = bcrypt.hashpw(info.password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
    
    User.create(
        session, auto_commit=True, 
        password=hash_pw, 
        user_id=info.user_id,
    )

async def check_user_info(info: Login, session):
    if not await is_username_exist(info.user_id):
        return False
    user = User.get(user_id=info.user_id)
    pw_check = bcrypt.checkpw(info.password.encode('utf-8'), user.password.encode('utf-8'))
    
    if user and pw_check:
        token = authhandler.encode_token(user.id)
        return token
    return False


def check_pw_format(password):
    if re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$',password):
        return True 
    return False

async def url_pattern_check(path, re_pattern):
    result = re.match(re_pattern, path)
    
    if result:
        return True
    return False

def check_user_history(id: int):

    user_history = Image.get(user_id=id)
    
    if user_history:
        return True
    return False    