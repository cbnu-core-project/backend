from fastapi import APIRouter
from config.database import collection_club_activity_history
from bson.json_util import loads, dumps
from models.club_activity_history_model import ClubActivityHistory
from schemas.club_activity_history_schema import club_activities_history_serializer
from bson import ObjectId

router = APIRouter(
    tags=["Club_Activity_History"]
)

@router.get("/api/club_activity_history", description="전체 동아리 활동 내역 가져오기")
def read_club_activity_history():
    club_activity_history = club_activities_history_serializer(loads(dumps(collection_club_activity_history.find())))
    return club_activity_history

@router.get("/api/club_activity_history/{club_objid}", description="동아리 별로 동아리 활동 내역 가져오기")
def read_club_activity_history(club_objid: str):
    club_activity_history = club_activities_history_serializer(loads(dumps(collection_club_activity_history.find({"club_objid":club_objid}))))
    return club_activity_history

@router.post("/api/club_activity_history", description="동아리 별로 동아리 활동 내역 새로 추가하기")
def create_club_activity_history(club_activity_history: ClubActivityHistory):
    _id = collection_club_activity_history.insert_one(dict(club_activity_history))
    club_activity_history = club_activities_history_serializer(collection_club_activity_history.find({"_id": _id.inserted_id}))
    return club_activity_history

@router.delete("/api/club_activity_history/{objid}", description="동아리 별로 동아리 활동 내역 하나 삭제하기")
def delete_club_activity_history(objid: str):
    collection_club_activity_history.delete_one({"_id" : ObjectId(objid)})
    return []

@router.put("/api/club_activity_history/{objid}", description="동아리 별로 동아리 활동 내역 하나 수정하기")
def put_club_activity_history(objid: str, club_activity_history: ClubActivityHistory):
    collection_club_activity_history.update_one({"_id":ObjectId(objid)}, {"$set":dict(club_activity_history)})
    club_activity_history = club_activities_history_serializer(collection_club_activity_history.find({"_id": ObjectId(objid)}))
    return club_activity_history
    
