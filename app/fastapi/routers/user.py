from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models import UserRequest
from db_sample import USER_DB  

router = APIRouter()

# 사용자 정의 예외 처리 함수
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# 사용자 생성 (회원가입)
@router.post("/user")
def join_user(request: UserRequest):
    username = request.username
    password = request.password
    name = request.name
    phone_number = request.phone_number
    dob = request.dob  # 생년월일

    # 중복된 ID 확인
    if username in USER_DB:
        raise HTTPException(status_code=409, detail="이미 존재하는 아이디입니다.")

    # 이름, 전화번호, 생년월일이 동일한 사용자가 있는지 확인
    for user_data in USER_DB.values():
        if user_data["name"] == name and user_data["phone_number"] == phone_number and user_data["dob"] == dob:
            raise HTTPException(status_code=409, detail="이미 가입된 사용자입니다.")

    # 전화번호가 이미 있는지 확인
    if any(user_data["phone_number"] == phone_number for user_data in USER_DB.values()):
        raise HTTPException(status_code=409, detail="이미 존재하는 전화번호입니다.")

    # 사용자 저장
    USER_DB[username] = {
        "password": password,
        "name": name,
        "phone_number": phone_number,
        "dob": dob
    }
    
    return {
        "status_code": 0,
        "data": {
            "username": username,
        },
        "message": "signup_success"
    }
