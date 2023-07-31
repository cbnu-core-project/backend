from fastapi import APIRouter, HTTPException
from config.database import collection_club_application_submit
from bson.json_util import loads, dumps
from models.club_application_submit_model import ClubApplicationSubmit
from schemas.others_schema import others_serializer
from bson import ObjectId

router = APIRouter(
	tags=["club_application_submit"]
)

@router.get('/api/club_application_submit')
def get_club_application_submit_all():
	club_application_submit = others_serializer(collection_club_application_submit.find())
	return club_application_submit

@router.get('/api/club_application_submit/{objid}')
def get_club_application_submit(objid: str):
	club_application_submit = others_serializer((collection_club_application_submit.find({"_id": ObjectId(objid)})))
	return club_application_submit

@router.get('/api/club_application_submit/club_objid/{club_objid}')
def get_club_application_submit_clubobjid(club_objid: str):
    club_application_submit = others_serializer((collection_club_application_submit.find({"club_objid": club_objid})))
    return club_application_submit

@router.post('/api/club_application_submit')
def create_club_application_submit(club_application_submit: ClubApplicationSubmit):
    club_application_submit = dict(club_application_submit)

    # 먼저, 동아리 양식이 이미 존재하는지 아닌지 확인
    user_objid = club_application_submit["user_objid"]
    club_objid = club_application_submit["club_objid"]
    user_objid_data = others_serializer(collection_club_application_submit.find({"user_objid": user_objid}))
    club_objid_data = others_serializer(collection_club_application_submit.find({"club_objid": club_objid}))
	
    # 유저가 동일한 동아리에 2개의 신청서를 놓지 못하도록 처리
    if((user_objid_data) and (club_objid_data)):
        raise HTTPException(status_code=400, detail={"message": "이미 양식을 제출했습니다. 기존 양식을 수정하거나 삭제 후 다시 써 주세요."})

	# 리스트를 쓸 수 있게 가공하기
    questions = club_application_submit["questions"]
    new_questions = [ dict(question) for question in questions ]

	# 새로 pymongo에서 쓸 수 있게 가공된 리스트로 대체 후 추가
    club_application_submit['questions'] = new_questions
    data = collection_club_application_submit.insert_one(club_application_submit)

	# 제대로 추가 되었는 지, 찾아서 확인 후 출력
    inserted_data = others_serializer(collection_club_application_submit.find({"_id": data.inserted_id}))

    return inserted_data

@router.put('/api/club_application_submit/{objid}')
def update_club_application_form(objid: str, club_application_submit: ClubApplicationSubmit):
	club_application_submit = dict(club_application_submit)

	# 리스트를 쓸 수 있게 가공하기
	questions = club_application_submit["questions"]
	new_questions = [dict(question) for question in questions]

	# 새로 pymongo에서 쓸 수 있게 가공된 리스트로 대체
	club_application_submit['questions'] = new_questions

	# 수정하기
	collection_club_application_submit.update_one({"_id": ObjectId(objid)}, {"$set": club_application_submit})

	return {"message": "수정 완료"}

@router.delete('/api/club_application_submit/{objid}')
def delete_club_application_submit(objid: str):
	collection_club_application_submit.delete_one({"_id": ObjectId(objid)})
	return {"message": "삭제 완료"}

