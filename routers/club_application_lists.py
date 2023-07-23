from fastapi import APIRouter
from config.database import collection_club_application_list
from models.club_application_lists_model import ClubApplicationList
from schemas.others_schema import others_serializer

router = APIRouter(
    tags=["club_application_lists"]
)

@router.get("/api/club_application_lists")
def read_club_application_lists_all():
    club_application_lists = others_serializer(collection_club_application_list.find())
    return club_application_lists

@router.get("/api/club_application_lists/{club_objid}", description="동아리 구분 신청리스트 가져오기")
def read_club_application_lists(club_objid: str):
    club_application_lists = others_serializer(collection_club_application_list.find({"club_objid": club_objid}))
    return club_application_lists

@router.get("/api/club_application_lists/user_objid/{user_objid}")
def read_user_club_application_lists(user_objid: str):
    club_application_lists = others_serializer(collection_club_application_list.find({"user_objid": user_objid}))
    return club_application_lists

@router.get("/api/club_application_lists/username/{username}")
def read_user_club_application_lists(username: str):
    club_application_lists = others_serializer(collection_club_application_list.find({"username": username}))
    return club_application_lists

@router.post("/api/club_application_lists")
def create_user_club_application_list(club_application_list: ClubApplicationList):
    collection_club_application_list.insert_one(dict(club_application_list))
    return "추가 성공"

