import io
import cv2
import requests
import streamlit as st
from PIL import Image
from common.const import BACKEND_URL

menu = ["Login", "SignUp", "Detect", "History"]

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
historySection = st.container()


def db_pred_img_viz(img_path, img_info, img_date):
    cate_col = {1: (192, 0, 128), 2: (192, 128, 64), 3: (0, 128, 64)}
    origin_img = cv2.imread(img_path)
    troub_type = [0, 0, 0]
    
    for tr in img_info:
        rect = tr['bbox']
        troub_type[int(tr['trouble_type'])-1] += 1
        cv2.rectangle(origin_img, (rect[0], rect[1]), (rect[2], rect[3]), color=cate_col[tr['trouble_type']], thickness=1)
        cv2.putText(origin_img, f"type{tr['trouble_type']}", (rect[0], rect[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, cate_col[tr['trouble_type']], thickness=1)

    origin_img = cv2.cvtColor(origin_img, cv2.COLOR_BGR2RGB)
    return {'image': origin_img, 'datetime': img_date, 'trouble_type': troub_type}


def main(auth_token):
    with mainSection:
        uploaded_file = st.file_uploader('Choose an image', type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            image_bytes = uploaded_file.getvalue()
            image = Image.open(io.BytesIO(image_bytes))

            st.image(image, caption='your image')
            st.write('Detecting...')

            files = {"file": uploaded_file.getvalue(),}
            
            res = requests.post(f"{BACKEND_URL}/img/order", files=files, headers={"Authorization": f'Bearer {auth_token}'})
            img_info = res.json()
            
            st.image(img_info.get('img_path'), caption='detected image')
            st.write(f"type1 개수: {img_info.get('type1')}")
            st.write(f"type2 개수: {img_info.get('type2')}")
            st.write(f"type3 개수: {img_info.get('type3')}")
            st.write(f"총합: {img_info.get('type1') + img_info.get('type2') + img_info.get('type3')}")


def show_signup_page():
    st.subheader("Create New Account")
    user_id = st.text_input('User Name')
    password = st.text_input('password', type="password")
    if st.button('Register'):
        res = requests.post(f"{BACKEND_URL}/auth/signup", 
                            json={'user_id': user_id, 'password': password})
        response = res.json()
        
        if response['msg'] == 'ID ALREADY EXISTS':
            st.error('이미 존재하는 아이디입니다.')
        elif response['msg'] == 'ID AND PASSWORD REQUIRED':
            st.error('잘못된 아이디 혹은 비밀번호 양식입니다.')
        elif response['msg'] == 'SUCCESSFULLY REGISTERED':
            st.success('성공적으로 가입되었습니다.')


def show_login_page():
    with loginSection:
        user_id = st.text_input('User Name')
        password = st.text_input('password', type="password")
        if st.button("Login"):
            res = requests.post(f"{BACKEND_URL}/auth/login", 
                                json={'user_id': user_id, 'password': password})
            response = res.json()
            
            if response['msg'] == "ID AND PASSWORD REQUIRED":
                st.error('아이디 혹은 비밀번호를 제대로 입력해주세요.')
            elif response['msg'] == "WRONG ID OR PASSWORD":
                st.error('잘못된 아이디 혹은 비밀번호 입니다.')
            elif response['msg'] == "SUCCESSFULLY LOGGED IN":
                st.success(f'{user_id} 계정으로 로그인되었습니다.')
                st.session_state['auth_token'] = response['Authorization']
                st.session_state['loggedIn'] = True


def show_history_page(auth_token):
    with historySection:
        res = requests.get(f"{BACKEND_URL}/img/history", headers={"Authorization": f'Bearer {auth_token}'})
        inference_info = res.json()
        st.json(inference_info)
        if inference_info['msg'] == 'NO HISTORY':
            st.error('내역이 없습니다 Detect를 수행하세요!')
        else:
            st_img = inference_info[0]['image_path']
            img_info = []
            temp = {}
            inferenced_img = []
            for info in inference_info:
                temp = dict(image_path=st_img)
                
                if info['image_path'] == st_img:
                    img_date = info['image_updated_at']
                    temp['trouble_type'] = info['trouble_type']
                    temp['bbox'] = [info['xmin'], info['ymin'], info['xmax'], info['ymax']]
                    img_info.append(temp)
                else:
                    temp_img = db_pred_img_viz(st_img, img_info, img_date)
                    inferenced_img.append(temp_img)
                    st_img = info['image_path']
                    img_info = []
                
            
            temp_img = db_pred_img_viz(st_img, img_info, img_date)
            inferenced_img.append(temp_img)
            
            for i in inferenced_img[::-1]:
                st.write(i['datetime'])
                st.image(i['image'])
                st.write(f"type1 개수: {i['trouble_type'][0]}")
                st.write(f"type2 개수: {i['trouble_type'][1]}")
                st.write(f"type3 개수: {i['trouble_type'][2]}")
                st.write(f"총합: {sum(i['trouble_type'])}")
                st.write()
            
              
with headerSection:
    st.title("skin trouble detection")
    choice = st.sidebar.selectbox('Menu', menu)
    if choice == 'SignUp':
        show_signup_page()
    elif choice == 'Login' or choice == 'Detect':
        if 'auth_token' not in st.session_state:
            show_login_page()
        else:
            main(st.session_state['auth_token'])
    elif choice == 'History':
        if 'auth_token' not in st.session_state:
            show_login_page()
        else:
            show_history_page(st.session_state['auth_token'])
