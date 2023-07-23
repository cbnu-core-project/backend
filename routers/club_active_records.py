from fastapi import APIRouter
from schemas.others_schema import others_serializer
from config.database import collection_club_active_record
from models.club_active_records_model import ClubActiveRecord
from bson import ObjectId

router = APIRouter(
    tags=["club_active_records"]
)


@router.get("/api/club_active_records", description="동아리 활동기록 전체(동아리구분없이) 가져오기")
def read_club_active_records_all():
    club_active_records = others_serializer(collection_club_active_record.find())
    return club_active_records

@router.get("/api/club_active_records/{club_objid}", description="동아리 활동기록 (동아리 구별)")
def read_club_active_records_all(club_objid: str):
    club_active_records = others_serializer(collection_club_active_record.find({"club_objid": club_objid}))
    return club_active_records

@router.get("/api/club_active_records/some/{club_objid}", description="동아리 활동기록 (동아리 구별)")
def read_club_active_records_all(club_objid: str, skip: int, limit: int):
    club_active_records = others_serializer(collection_club_active_record.find({"club_objid": club_objid}).skip(skip).limit(limit))
    return club_active_records

@router.post("/api/club_active_records")
def create_club_active_records(club_active_record: ClubActiveRecord):
    inserted_data = collection_club_active_record.insert_one(dict(club_active_record))
    return "추가 성공"

@router.put("/api/club_active_records/{objid}")
def update_club_active_records(objid: str, club_active_record: ClubActiveRecord):
    collection_club_active_record.update_one({"_id": ObjectId(objid)}, {"$set": dict(club_active_record)})
    return "수정 성공"

@router.delete("/api/club_active_records/{objid}")
def delete_club_active_records(objid: str):
    collection_club_active_record.delete_one({"_id": objid})
    return "삭제 성공"

