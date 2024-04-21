
import re
import string
import pandas as pd

def check_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

def check_name(name):
    if not name:
        return False
    if len(name) <= 8:
        if all(char in string.ascii_letters or char in string.whitespace for char in name):
            return True
    return False

def check_id(id):
    if not id:
        return False
    if len(id) < 4:
        return False
    if len(id) > 8:
        return False
    pattern = r'^[a-zA-Z]{2,}[0-9]{1,}$'
    if re.match(pattern, id):
        return True
    else:
        return False

def check_pwd(pwd):
    if not pwd:
        return False
    if len(pwd) >= 8 and len(pwd) <= 20:
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$'
        if re.fullmatch(pattern, pwd):
            return True
    else:
        return False

def check_input(email, name, user_id, password, phone_number):
    return (check_email(email) and
            check_name(name) and
            check_id(user_id) and
            check_pwd(password))

def add_user_info(df, email, name, user_id, password):
    if check_email(email) and check_name(name) and check_id(user_id):
        df = pd.concat([df, pd.DataFrame({
            'name': [name],
            'email': [email],
            'id': [user_id],
            'password': [password],
        })], ignore_index=True)
        return df

def check_info(email, name, user_id, password):
    i=0
    if not check_email(email):
        print("이메일 형식을 확인해주세요.")
        i+=1
    if not check_name(name):
        print("이름 형식을 확인해주세요.")
        i+=1
    if not check_id(user_id):
        print("아이디 형식을 확인해주세요")
        i+=1
    if not check_pwd(password):
        print("비밀번호 형식을 확인해주세요.")
        i+=1
    if i!=0:
        return False
    else:
        return True

def append_to_csv(df, file_name):
    try:
        df.to_csv(file_name, mode='a', header=False, index=False)
        print(f"데이터가 '{file_name}' 파일에 추가되었습니다.")
    except Exception as e:
        print(f"데이터를 추가하는 도중 오류가 발생했습니다: {e}")
