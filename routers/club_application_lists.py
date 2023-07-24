from fastapi import APIRouter
from config.database import collection_club_application_list
from models.club_application_lists_model import ClubApplicationList
from schemas.others_schema import others_serializer
from bson import ObjectId

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

@router.post("/api/club_application_lists")
def create_user_club_application_list(club_application_list: ClubApplicationList):
    collection_club_application_list.insert_one(dict(club_application_list))
    return "추가 성공"

@router.put("/api/club_application_lists/{objid}", description="동아리 별로 동아리 활동 내역 하나 수정하기")
def put_club_application_list(objid: str, club_application_list: ClubApplicationList):
    collection_club_application_list.update_one({"_id":ObjectId(objid)}, {"$set":dict(club_application_list)})
    club_application_list = others_serializer(collection_club_application_list.find({"_id": ObjectId(objid)}))
    return club_application_list

@router.delete("/api/club_application_lists/{objid}", description="동아리 별로 동아리 활동 내역 하나 삭제하기")
def delete_club_application_list(objid: str):
    collection_club_application_list.delete_one({"_id" : ObjectId(objid)})
    return []
