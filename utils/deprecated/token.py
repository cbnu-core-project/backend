from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from config.database import collection_user
from schemas.users_schema import users_serializer
from jose import jwt, JWTError

# .env
# from dotenv import load_dotenv
# import os

# load_dotenv(".env")


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
"""
배포할 때는 dotenv 사용하기
"""
# SECRET_KEY = os.environ.get('SECRET_KEY')
# REFRESH_SECRET_KEY = os.environ.get('REFRESH_SECRET_KEY')
SECRET_KEY = "secretkey825"
REFRESH_SECRET_KEY = "refreshsecretkey825"


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/login", scheme_name="JWT")

# access token 만들기
def create_access_token(user):
	data = {
		"sub": user["username"],
		"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
	}
	access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
	return access_token

# refresh token 만들기
def create_refresh_token(user):
	data = {
		"sub": user["username"],
		"exp": datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
	}
	refresh_token = jwt.encode(data, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
	return refresh_token

# refresh token 검증 db와 검증 및 access_token 재발급
def verify_refresh_token_and_create_access_token(refresh_token):
	try:
		payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
		username = payload["sub"]

		user = users_serializer(collection_user.find({"username": username}))[0]
		if user:
			# db의 리프레시토큰이랑 받은 리프레시토큰이랑 비교
			if (user.get("refresh_token")==refresh_token):
				# 유저정보랑 new_access_token 같이 반환
				return { "access_token": create_access_token(user), "user": user}
		raise HTTPException(status_code=401, detail="유효하지 않은 리프레시토큰이다.")
	except JWTError:
		raise HTTPException(status_code=401, detail="유효하지 않은 리프레시토큰이다.2")



# access 토큰 검증 함수
def verify_token(token: str = Depends(oauth2_schema)):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		sub = payload.get("sub")

		if sub is None:
			raise HTTPException(status_code=401, detail="로그인 되어있지 않다.")

		if sub:
			user = users_serializer(collection_user.find({"username": sub}))
			if user is None:
				raise HTTPException(status_code=401, detail="유효하지 않은 토큰이다.1")

		exp = payload.get("exp")
		if exp is None or datetime.utcnow() > datetime.fromtimestamp(exp):
			raise HTTPException(status_code=401, detail="토큰이 이미 만료되었다.")

		return user[0]  # user는 dict형태로 반환
	except JWTError:
		raise HTTPException(status_code=401, detail="유저를 찾을 수 없습니다.")

# 스케줄을 작성/수정하기 위한 권한 확인, 내가 속해있는 동아리가 맞는 지 확인
def verify_schedule_authority(club_objid: str, token: str = Depends(oauth2_schema)):
	user = verify_token(token)
	# 현재 속해 있는 클럽(동아리)와 data(post, schedule)추가/수정 대상의 동아리 비교
	if club_objid in user.get("clubs"):
		if user.get("authority") <= 2:
			return user

	raise HTTPException(status_code=401, detail="속해있는 동아리가 아니다.")




