from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from config.database import collection_user
from pydantic import BaseModel
from utils.common_token import verify_common_token_and_get_unique_id, verify_common_refresh_token_and_create_access_token, common_access_token_logout, common_header_access_token_logout
from schemas.others_schema import others_serializer


router = APIRouter(
    tags=["users"]
)


@router.get("/api/user/info", description="로그인 된 사용자의 정보 가져오기")
def get_user(unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    user = others_serializer(collection_user.find({"unique_id": unique_id}))[0]

    return user


# 현재 유저가 속한 동아리 리스트 가져오기
@router.get("/api/user/clubs")
def get_user_clubs(unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    user = others_serializer(collection_user.find({"unique_id": unique_id}))[0]
    clubs = user.get("clubs")

    return clubs


class UserClubs(BaseModel):
    clubs: list[str]


# 유저 동아리 리스트 수정하기 ( 받아온 리스트로 대체 )
@router.put("/api/user/clubs", description="유저 동아리 리스트 수정하기 (보낸 리스트로 전부 대체)")
def update_user_clubs(clubs: UserClubs, unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    user = others_serializer(collection_user.find({"unique_id": unique_id}))[0]
    clubs_list = dict(clubs).get("clubs")
    collection_user.update_one({"_id": ObjectId(user["_id"])}, {
                               "$set": {"clubs": clubs_list}})
    return "update"

# 유저 동아리 리스트에 동아리 1개 추가하기
@router.post("/api/user/club/push", description="유저 동아리 리스트에 동아리 1개 추가")
def push_user_club(club_objid: str, unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    user = others_serializer(collection_user.find({"unique_id": unique_id}))[0]
    collection_user.update_one({"_id": ObjectId(user["_id"])}, {
                               "$push": {"clubs": club_objid}})

    return "push"

# 현재 유저가 속한 관심동아리 리스트 가져오기
@router.get("/api/user/interests")
def get_user_clubs(unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    user = others_serializer(collection_user.find({"unique_id": unique_id}))[0]
    interests = user.get("interests")

    return interests

# 유저 관심동아리 리스트에 관심동아리 1개 추가하기
@router.post("/api/user/interest/push", description="유저 관심동아리 리스트에 관심동아리 1개 추가 / except: 이미 존재하고 있는 관심동아리라면, 400실패를 보냄")
def push_user_club(club_objid: str, unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    user = others_serializer(collection_user.find({"unique_id": unique_id}))[0]
    if (club_objid in user.get('interests')):
        raise HTTPException(status_code=400, detail="이미 존재하는 동아리 입니다.")
    collection_user.update_one({"unique_id": unique_id}, {
                               "$push": {"interests": club_objid}})

    return "push"

# 유저 관심동아리 삭제
@router.delete("/api/user/interest/delete/{club_objid}", description="관심동아리의 club_objid를 보내주면 그것을 삭제 (인덱스x)")
def push_user_club(club_objid: str, unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    collection_user.update_one({"unique_id": unique_id}, {
                               "$pull": {"interests": club_objid}})

    return "delete"


class RefreshToken(BaseModel):
    refresh_token: str


@router.post("/api/refresh")
def refresh(token: RefreshToken):
    refresh_token = dict(token).get("refresh_token")
    new_access_token = verify_common_refresh_token_and_create_access_token(
        refresh_token)
    print(new_access_token)

    return {"access_token": new_access_token}


@router.get("/api/common/protected")
def common_protected(unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    return "토큰 유효해요."


class AccessToken(BaseModel):
    access_token: str

# 받아온 access_token 의 만료처리
@router.post("/api/access_token/logout")
def access_token_logout(token: AccessToken):
    access_token = dict(token).get('access_token')
    message = common_access_token_logout(access_token)
    return {"message": message}

# 헤더를 통한 로그아웃
@router.post("/api/header/access_token/logout")
def common_logout(message: str = Depends(common_header_access_token_logout)):
    return "로그아웃"
