from fastapi import APIRouter, File, UploadFile
from config.database import collection_club_programs
from models.club_programs_model import ClubPrograms
from schemas.club_programs_schema import club_programs_serializer
from bson.json_util import loads, dumps
from bson import ObjectId

router = APIRouter(
    tags=["Club_Programs"]
)

@router.get("/api/club_programs", description="모든 동아리 활동 프로그램 가져오기")
def read_all_club_programs():
    club_programs = club_programs_serializer(loads(dumps(collection_club_programs.find())))
    return club_programs

@router.get("/api/club_programs/{club_objid}", description="해당 동아리 활동 프로그램 가져오기")
def read_one_club_programs(club_objid: str):
    club_programs = club_programs_serializer(loads(dumps(collection_club_programs.find({"club_objid":club_objid}))))
    return club_programs

@router.post("/api/club_programs", description="활동 프로그램 추가하기")
def create_club_programs(club_programs: ClubPrograms):
    _id = collection_club_programs.insert_one(dict(club_programs))
    club_programs = club_programs_serializer(collection_club_programs.find({"_id":_id.inserted_id}))
    return club_programs

@router.delete("/api/club_programs/{objid}", description="해당 동아리 활동 프로그램 1개만 삭제하기")
def delete_club_programs(objid: str):
    collection_club_programs.delete_one({"_id":ObjectId(objid)})
    return {"message": "삭제 성공"}

@router.put("/api/club_programs/{objid}", description="해당 동아리 활동 프로그램 선택 수정하기")
def put_club_programs(objid: str, club_programs: ClubPrograms):
    collection_club_programs.update_one({"_id":ObjectId(objid)},{"$set":dict(club_programs)})
    club_programs = club_programs_serializer(collection_club_programs.find({"_id": ObjectId(objid)}))

    return club_programs
