from bson import ObjectId
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from config.database import collection_user
from schemas.users_schema import users_serializer
from models.users_model import User
from pydantic import BaseModel

# utils
from utils.password import hash_password, verify_password
from utils.deprecated.token import create_access_token, verify_token, oauth2_schema, create_refresh_token, verify_refresh_token_and_create_access_token

router = APIRouter(
	tags=["users"]
)


@router.post("/api/register")
def user_register(user: User):
	if(users_serializer(collection_user.find({"username": user.username}))):
		raise HTTPException(status_code=409,
							detail="이미 존재하는 사용자입니다.")
	collection_user.insert_one({"username": user.username,
								"password": hash_password(user.password),
								"realname": user.realname,
								"clubs": user.clubs,
								"refresh_token": user.refresh_token,
								"authority": user.authority})
	return "회원가입 성공!"


@router.post("/api/login")
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
	# 데이터베이스에서 유저데이터 가져오기
	user = users_serializer(collection_user.find({"username": form_data.username}))
	# 데이터베이스에 데이터가 있다면, user 데이터에 user 1개 저장
	if user:
		user = user[0]
	if not user or not verify_password(form_data.password, user["password"]):
		raise HTTPException(
			status_code=401,
			detail="잘못 된 username, password",
			headers={"WWW-Authenticate": "Bearer"},
		)

	# token 만들기
	access_token = create_access_token(user)
	refresh_token = create_refresh_token(user)

	collection_user.update_one({"_id": user.get("_id")}, { "$set": { "refresh_token": refresh_token}})

	return {
        "access_token": access_token,
		"refresh_token": refresh_token,
        "token_type": "bearer",
        "username": user["username"],
    }


# 보호된 엔드포인트
@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_schema)):
	payload = verify_token(token)
	# 토큰이 유효하다면, 여기에서 필요한 처리를 수행합니다.
	print('토큰 유효한듯?')
	return token

@router.get("/api/user/info/{username}", description="username(id) 에 맞는 유저의 정보 리턴")
def get_user(username: str):
	user = users_serializer(collection_user.find({"username": username}))[0]
	return user

@router.get("/api/user/info", description="로그인 된 사용자의 정보 가져오기")
def get_user(token: str = Depends(oauth2_schema)):
	user = verify_token(token)
	return { "_id": user["_id"],"username": user["username"], "realname": user["realname"], "clubs": user["clubs"]}


# 현재 유저가 속한 동아리 리스트 가져오기
@router.get("/api/user/clubs")
def get_user_clubs(token: str = Depends(oauth2_schema)):
	user = verify_token(token)
	clubs = user.get("clubs")

	return clubs

class UserClubs(BaseModel):
	clubs: list[str]


# 유저 동아리 리스트 수정하기 ( 받아온 리스트로 대체 )
@router.put("/api/user/clubs", description="유저 동아리 리스트 수정하기 (보낸 리스트로 전부 대체)")
def update_user_clubs(clubs: UserClubs, token: str = Depends(oauth2_schema)):
	user = verify_token(token)
	clubs_list = dict(clubs).get("clubs")
	collection_user.update_one({"_id": ObjectId(user["_id"])}, {"$set": {"clubs": clubs_list}})
	return "update"

# 유저 동아리 리스트에 동아리 1개 추가하기
@router.post("/api/user/club/push/{objid}", description="유저 동아리 리스트에 동아리 1개 추가")
def push_user_club(objid: str, token: str = Depends(oauth2_schema)):
	user = verify_token(token)
	collection_user.update_one({"_id": ObjectId(user["_id"])}, {"$push": {"clubs": objid}})

	return "push"

class RefreshToken(BaseModel):
	refresh_token: str

@router.post("/api/refresh")
def refresh(token: RefreshToken):
	refresh_token = dict(token).get("refresh_token")
	payload = verify_refresh_token_and_create_access_token(refresh_token)

	new_access_token = payload.get("access_token")
	return new_access_token


