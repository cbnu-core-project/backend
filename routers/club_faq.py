from fastapi import APIRouter,HTTPException
from schemas.club_faq import club_faqs_serializer
from config.database import collection_club_faq
from schemas.others_schema import others_serializer
from models.club_faq_model import ClubFaq
from bson import ObjectId
from bson.json_util import loads, dumps

router = APIRouter(
    tags=["club_faq"]
)

@router.get("/api/club_faq", description="동아리 faq 전체(동아리구분없이) 가져오기")
def read_club_faq_all():
    club_faqs = club_faqs_serializer(loads(dumps(collection_club_faq.find())))
    return club_faqs

@router.get("/api/club_faq/{club_objid}", description="해당 동아리 활동 프로그램 가져오기")
def read_one_club_programs(club_objid: str):
    club_faqs = club_faqs_serializer(loads(dumps(collection_club_faq.find({"club_objid":club_objid}))))
    return club_faqs

@router.post("/api/club_faq", description="동아리 별로 동아리 활동 내역 새로 추가하기")
def create_club_faq(club_faq: ClubFaq):
    club_faq = dict(club_faq)
    
    club_objid = club_faq["club_objid"]
    finded_data = others_serializer(collection_club_faq.find({"club_objid": club_objid}))
    if (finded_data):
        raise HTTPException(status_code=400, detail="이미 faq가 존재합니다. 기존 faq를 수정하거나 삭제 후 다시 써 주세요.")
    faqs = club_faq["faqs"]
    new_faqs = [ dict(faq) for faq in faqs ]
    
    club_faq["faqs"] = new_faqs
    data = collection_club_faq.insert_one(club_faq)
    inserted_data = club_faqs_serializer(collection_club_faq.find({"_id": data.inserted_id}))
    return inserted_data

@router.delete("/api/club_faq/{objid}")
def delete_club_faq(objid: str):
    collection_club_faq.delete_one({"_id" : ObjectId(objid)})
    return []

@router.put("/api/club_faq/{objid}")
def update_club_faq(objid: str, club_faq: ClubFaq):
    club_faq = dict(club_faq)
    faqs = club_faq["faqs"]
    new_faqs = [ dict(faq) for faq in faqs ]
    
    club_faq["faqs"] = new_faqs
    data = collection_club_faq.update_one({"_id":ObjectId(objid)},{"$set":club_faq})
    inserted_data = club_faqs_serializer(collection_club_faq.find({"_id": data.inserted_id}))
    return inserted_data
