import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.database import collection_user
from enums.enums import SocialEnum
from schemas.others_schema import others_serializer
from utils.naver_token import verify_and_get_naver_token

NAVER_CLIENT_ID = "zB5gfqdBq1a0jq6vr_zv";
NAVER_CLIENT_SECRET = "X8C0M1JHIH"
NAVER_REDIRECT_URI = "http://localhost:3000";
NAVER_USERINFO_URL = "https://openapi.naver.com/v1/nid/me"

# + code 랑 같이 쓰여야 됨
NAVER_GET_TOKEN_URL = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&state=naver&code="



router = APIRouter(
	tags=["naver_oauth"]
)

class Code(BaseModel):
	code: str

def get_naver_user_info(access_token):
	headers = {"Authorization": f"Bearer {access_token}"}
	response = requests.get(NAVER_USERINFO_URL, headers=headers)

	if not response.ok:
		raise HTTPException(
			status_code=401,
			detail="잘못 된 access_token",
			headers={"WWW-Authenticate": "Bearer"},
		)

	return response.json()

def user_register(user):

	social = SocialEnum.naver.value
	user_response = user.get('response')
	id = user_response.get('id')

	# 이미 가입된 이메일이면
	if(others_serializer(collection_user.find({"unique_id": f"{social}_{id}"}))):
		return False

	# 가입되지 않은 이메일이면
	collection_user.insert_one({"unique_id": f"{social}_{id}",
								"email": user_response.get('email'),
								"realname": "",
								"nickname": user_response.get('nickname'),
								"profile_image_url": user_response.get('profile_image'),
								"social": social,
								"clubs": [],
								"refresh_token": "",
								"authority": 4,
								"major": "",
								"student_number": "",
								"phone_number": "",
								})
	return True

@router.post("/oauth/naver/login")
def kakao_oauth(code: Code):
	code = dict(code).get('code')
	response = requests.post(NAVER_GET_TOKEN_URL + code).json()

	access_token = response.get('access_token')
	refresh_token = response.get('refresh_token')

	# 유저 정보를 통한 회원가입
	user_info = get_naver_user_info(access_token)
	if (user_register(user_info)):
		print("회원가입 완료")

	return { "access_token": access_token, "refresh_token": refresh_token }


@router.get(
    "/oauth/naver/protected",
    response_model=str,
)
async def protected(token: str = Depends(verify_and_get_naver_token)):
	print(get_naver_user_info(token))
	return f"Hello, user! Your token is {token}."