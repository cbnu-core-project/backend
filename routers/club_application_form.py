from fastapi import APIRouter, HTTPException
from config.database import collection_club_application_form
from models.club_application_form_model import ClubApplicationForm
from schemas.others_schema import others_serializer
from bson import ObjectId

router = APIRouter(
	tags=["club_application_form"],
)

@router.get('/api/club_application_form/{club_objid}')
def get_club_application_form(club_objid: str):
	club_application_form = others_serializer(collection_club_application_form.find({"club_objid": club_objid}))
	return club_application_form

@router.post('/api/club_application_form')
def create_club_application_form(club_application_form: ClubApplicationForm):
	club_application_form = dict(club_application_form)

	# 먼저, 동아리 양식이 이미 존재하는지 아닌지 확인
	club_objid = club_application_form["club_objid"]
	finded_data = others_serializer(collection_club_application_form.find({"club_objid": club_objid}))
	if(finded_data):
		raise HTTPException(status_code=400, detail="이미 양식이 존재합니다. 기존 양식을 수정하거나 삭제 후 다시 써 주세요.")

	# 리스트를 쓸 수 있게 가공하기
	questions = club_application_form["questions"]
	new_questions = [ dict(question) for question in questions ]

	# 새로 pymongo에서 쓸 수 있게 가공된 리스트로 대체 후 추가
	club_application_form['questions'] = new_questions
	data = collection_club_application_form.insert_one(club_application_form)

	# 제대로 추가 되었는 지, 찾아서 확인 후 출력
	inserted_data = others_serializer(collection_club_application_form.find({"_id": data.inserted_id}))

	return inserted_data

@router.put('/api/club_application_form/{objid}', description="폼 고유의 objid를 통한 수정")
def update_club_application_form(objid: str, club_application_form: ClubApplicationForm):
	club_application_form = dict(club_application_form)

	# 리스트를 쓸 수 있게 가공하기
	questions = club_application_form["questions"]
	new_questions = [dict(question) for question in questions]

	# 새로 pymongo에서 쓸 수 있게 가공된 리스트로 대체
	club_application_form['questions'] = new_questions

	# 수정하기
	collection_club_application_form.update_one({"_id": ObjectId(objid)}, {"$set": club_application_form})

	return "수정 완료"

@router.put('/api/club_application_form/{club_objid}', description="동아리의 objid 를 통해 폼 수정")
def update_club_application_form(club_objid: str, club_application_form: ClubApplicationForm):
	club_application_form = dict(club_application_form)

	# 리스트를 쓸 수 있게 가공하기
	questions = club_application_form["questions"]
	new_questions = [dict(question) for question in questions]

	# 새로 pymongo에서 쓸 수 있게 가공된 리스트로 대체
	club_application_form['questions'] = new_questions

	# 수정하기
	collection_club_application_form.update_one({"club_objid": club_objid}, {"$set": club_application_form})

	return "수정 완료"

@router.delete('/api/club_application_form/{objid}')
def delete_club_application_form(objid: str):
	collection_club_application_form.delete_one({"_id": ObjectId(objid)})
	return []

