import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.database import collection_user
from enum import Enum
import json
from models.users_model import User
from enums.enums import SocialEnum
from schemas.others_schema import others_serializer
from utils.kakao_token import verify_and_get_kakao_token

# .env 환경변수 설정
from dotenv import load_dotenv, find_dotenv
import os
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)


KAKAO_REST_API_KEY = os.environ.get('KAKAO_REST_API_KEY')
KAKAO_REDIRECT_URI = os.environ.get('KAKAO_REDIRECT_URI')


KAKAO_USERINFO_URL = 'https://kapi.kakao.com/v2/user/me'
# + code 랑 같이 쓰여야 됨
KAKAO_GET_TOKEN_URL = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&code="

router = APIRouter(
	tags=["kakao_oauth"]
)

class Code(BaseModel):
	code: str

def get_kakao_user_info(access_token):
	headers = {"Authorization": f"Bearer {access_token}"}
	response = requests.get(KAKAO_USERINFO_URL, headers=headers,
							# params={"property_keys": json.dumps(["kakao_account.email"])}
	)

	if not response.ok:
		raise HTTPException(
			status_code=401,
			detail={"message": "잘못 된 access_token"},
			headers={"WWW-Authenticate": "Bearer"},
		)

	return response.json()

def kakao_user_register(user):

	social = SocialEnum.kakao.value
	id = user.get('id')

	# 이미 가입된 이메일이면
	if(others_serializer(collection_user.find({"unique_id": f"{social}_{id}"}))):
		return False

	# 가입되지 않은 이메일이면
	collection_user.insert_one({"unique_id": f"{social}_{id}",
								"email": user.get('kakao_account').get('email'),
								"realname": "",
								"nickname": user.get('kakao_account').get('profile').get('nickname'),
								"profile_image_url": user.get('kakao_account').get('profile').get('profile_image_url'),
								"social": social,
								"clubs": [],
								"refresh_token": "",
								"major": "",
								"student_number": "",
								"phone_number": "",
								"interests": [],
								"admin": False,
								"gender": "male",
								"address": ""
								})
	return True

@router.post("/oauth/kakao/login")
def kakao_oauth(code: Code):
	code = dict(code).get('code')
	headers = { "Content-type": "application/x-www-form-urlencoded;charset=utf-8" }
	response = requests.post(KAKAO_GET_TOKEN_URL + code, headers=headers).json()

	access_token = response.get('access_token')
	refresh_token = response.get('refresh_token')
	user_info = get_kakao_user_info(access_token)

	# 이메일 유효성 검증
	email = user_info.get('kakao_account').get('email')
	is_email_valid = user_info.get('kakao_account').get('is_email_valid')
	is_email_verified = user_info.get('kakao_account').get('is_email_verified')

	if (not(is_email_valid) or not(is_email_verified)):
		raise HTTPException(
			status_code=401,
			detail={"message": "유효하지 않거나 인증되지 않은 이메일"},
			headers={"WWW-Authenticate": "Bearer"},
		)

	# 유저정보를 통한 회원가입
	if (kakao_user_register(user_info)):
		print("회원가입 완료")

	return { "access_token": access_token, "refresh_token": refresh_token }


@router.get(
    "/oauth/kakao/protected",
    response_model=str,
)
async def protected(token: str = Depends(verify_and_get_kakao_token)):
	print(get_kakao_user_info(token))
	return {"message": f"Hello, user! Your token is {token}."}
