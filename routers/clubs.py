from bson import ObjectId
from fastapi import APIRouter, Query, Depends, HTTPException
from config.database import collection_club, collection_user
from models.clubs_model import Club
from schemas.clubs_schema import clubs_serializer
from schemas.others_schema import others_serializer
from utils.authority import return_club_member_info_and_club_authority, verify_club_authority
from utils.common_token import verify_common_token_and_get_unique_id
from logs.log import logger

router = APIRouter(
	tags=["clubs"]
)


@router.get("/api/clubs", description="동아리 전체 가져오기")
async def read_all_club():
	clubs = clubs_serializer(collection_club.find())

	logger.info("GET - /api/clubs")
	return clubs


@router.get("/api/clubs/classification/", description="동아리 분류별 전체 가져오기")
async def read_all_club(classification: int):
	clubs = clubs_serializer(collection_club.find({"classification": classification}))

	logger.info("GET - /api/clubs/classification/")
	return clubs


@router.get("/api/club/{objid}", description="오브젝트아이디에 맞는 동아리 1개만 가져오기(리스트로 받아옴)")
async def read_one_club(objid: str):
	# 비록 1개의 동아리만 가져오지만, 리스트형태로 받아온다.
	club = clubs_serializer(collection_club.find({"_id": ObjectId(objid)}))

	logger.info("GET - /api/club/{objid}")
	return club


@router.get("/api/clubs/some/", description="동아리 skip, limit를 통한 동아리 일부 가져오기\nex) 3번째부터 4개 가져오려면, -> skip=2, limit=4")
async def read_some_club(skip: int, limit: int):
	clubs = clubs_serializer(collection_club.find().skip(skip).limit(limit))

	logger.info("GET - /api/clubs/some/")
	return clubs


@router.get("/api/clubs/some/classification/", description="동아리 skip, limit를 통한 글 일부 가져오기\n그리고 classification을 통한 중앙 동아리 직무 동아리 구분 가능")
async def read_some_club(skip: int, limit: int, classification: int):
	clubs = clubs_serializer(collection_club.find({"classification": classification}).skip(skip).limit(limit))

	logger.info("GET - /api/clubs/some/classification/")
	return clubs


@router.get("/api/clubs/search/", description="검색어 쿼리로 넘기기")
async def search_club(query: str):
	condition = [
  {
    '$search': {
      'index': "clubSearch",
      'text': {
        'query': query,
        'path': ['title', 'content', 'tag1', 'tag2', 'tag3']
      }
    }
  },
		{ '$addFields': { 'score' : { '$meta': 'searchScore'}}}
]

	clubs = clubs_serializer(collection_club.aggregate(condition))

	logger.info("GET - /api/clubs/search/")
	return clubs


@router.get("/api/clubs/search/classification/", description="검색어 및 분류 쿼리로 넘기기")
async def search_club(query: str, classification: int):
	condition = [
  	{
    '$search': {
      'index': "clubSearch",
      'text': {
        'query': query,
        'path': ['title', 'content', 'tag1', 'tag2', 'tag3']
      		}
    	}
  	},
	{'$match': {'classification': classification}},
	{ '$addFields': { 'score' : { '$meta': 'searchScore'}}}
]

	clubs = clubs_serializer(collection_club.aggregate(condition))

	logger.info("GET - /api/clubs/search/classification/")
	return clubs


@router.post("/api/club", description="동아리 추가하기 / classification = 0 -> 중앙동아리, 1 -> 직무동아리")
async def create_club(club: Club):
	_id = collection_club.insert_one(dict(club))
	club = clubs_serializer(collection_club.find({"_id": _id.inserted_id}))

	logger.info("POST - /api/club")
	return club


@router.put("/api/club/{objid}", description="동아리 수정하기")
async def update_club(objid: str, club: Club):
	collection_club.update_one({"_id": ObjectId(objid)}, {"$set": dict(club)})
	club = clubs_serializer(collection_club.find({"_id": ObjectId(objid)}))

	logger.info("PUT - /api/club/{objid")
	return club

@router.delete("/api/club/{objid}", description="동아리 삭제하기 - ex) /api/post/123412 (삭제할 objectid) 경로로 'delete' 요청")
async def delete_club(objid: str):
	collection_club.delete_one({"_id": ObjectId(objid)})

	logger.info("DELETE - /api/club/{objid")
	return {"message": "삭제 완료"}

@router.post("/api/club/activity_tag/push", description="동아리 활동태그 추가(push)하기")
def delete_activity_tag(objid: str, activity_tag: str):
	collection_club.update_one({"_id": ObjectId(objid)}, {"$push" : {"activity_tags": activity_tag}})

	logger.info("POST - /api/club/activity_tag/push")
	return {"message": "추가 완료"}

@router.delete("/api/club/activity_tag/index", description="동아리 활동태그 인덱스를 통해 삭제하기")
def delete_activity_tag(objid: str, index: int):

	collection_club.update_one({"_id": ObjectId(objid)}, {"$unset": {f"activity_tags.{index}": 1}})
	collection_club.update_one({"_id": ObjectId(objid)}, {"$pull": {"activity_tags": None}})

	logger.info("DELETE - /api/club/activity_tag/index")
	return {"message": "태그 삭제 완료"}


@router.post("/api/club/image/push", description="쿼리파라미터로, 수정할 club의 objid랑, 추가할 image_url 주기")
def push_image_url(club_objid: str, image_url: str):
	collection_club.update_one({"_id": ObjectId(club_objid)}, { "$push" : { "image_urls": image_url}})

	logger.info("POST - /api/club/image/push")
	return {"message": "push success"}

@router.put("/api/club/image/update", description="쿼리파라미터로, 수정할 club의 objid랑, 대체할 image_url 주기")
def push_image_url(club_objid: str, image_url: str):
	collection_club.update_one({"_id": ObjectId(club_objid)}, { "$set" : { "image_urls": [image_url]}})

	logger.info("PUT - /api/club/image/update")
	return {"message": "image update success"}


@router.get("/api/club/member/{club_objid}", description="club_objid(str)를 path파라미터로 보내면, 그 동아리에 속한 멤버 정보가 담긴 리스트로 바꿔 줌, 그 동아리 내에서의 직급까지 같이 넣어서 보여줌.")
def get_users_info_from_users_list(club_objid: str):

	logger.info("GET - /api/club/member/{club_objid}")
	return return_club_member_info_and_club_authority(club_objid)


# 들어 있을 때만 삭제, 없으면 아무것도 안 하기
def remove_element(arr: list, element: str):
	if element in arr:
		arr.remove(element)
	else:
		pass

@router.post("/api/club/member", description=
"""	
		동아리 회장이상만 사용가능, 동아리 회장이 회장을 위임하거나, 동아리원들의 권한을 변경 할 때 사용
												 
		전부 쿼리파라미터로 넘겨주면 됨.
		club_objid : 수정할 동아리의 objid
		user_objid : 권한을 변경시킬 유저의 objid
		authority : 변경시킬 권한 ( 1 ~ 3 )  1회장으로 변경시킬 시에는 자신의 권한이 회장->동아리원으로 낮아짐
	""")
def update_club_member_authority(club_objid: str, user_objid: str, authority: int = Query(ge=1, le=3), unique_id = Depends(verify_common_token_and_get_unique_id)):

	my_data = verify_club_authority(unique_id=unique_id, club_objid=club_objid, inclusion_objid=True)
  
	if my_data.get("authority") >= 2:
		logger.critical("POST - /api/club/member : 동아리 회장만 직급을 수정할 수 있습니다. (프론트에서 예외처리 되었을 텐데, 로그 나오면 보안상 문제있는거) !!")
		raise HTTPException(status_code=401, detail={"message": "동아리 회장만 직급을 수정할 수 있습니다."})
  
	# 동아리 가져오기
	club = clubs_serializer(collection_club.find({"_id": ObjectId(club_objid)}))[0]
	president = club.get("president")
	executive = club.get("executive")
	member = club.get("member")
  
  
	"""
	수정해 주는 계급이 동아리 회장이라면?
  	일단, 회장과 임원에서 "나"를 찾아 다 삭제
  	그리고, 상대방을 동아리 회장으로 수정시켜줌
 	"""
	if authority == 1:
		remove_element(president, my_data.get("objid"))
		remove_element(executive, my_data.get("objid"))

		remove_element(president, user_objid)
		remove_element(executive, user_objid)

		president.append(user_objid)
	elif authority == 2:
		remove_element(president, user_objid)
		remove_element(executive, user_objid)

		executive.append(user_objid)

	elif authority == 3:
		remove_element(president, user_objid)
		remove_element(executive, user_objid)
   

	collection_club.update_one({"_id": ObjectId(club_objid)}, {"$set": { "president": president,
																		 "executive": executive}})

	updated_club = clubs_serializer(collection_club.find({"_id": ObjectId(club_objid)}))

	logger.info(f"POST - /api/club/member : 직급 변경 완료, {club.get('title')}에서 {my_data.get('user').get('realname')}({user_objid})의 변경된 직급 {authority}")

	return updated_club
  
@router.delete("/api/club/delete/member")
def delete_club(club_objid: str, user_objid: str, unique_id = Depends(verify_common_token_and_get_unique_id)):
	my_data = verify_club_authority(unique_id=unique_id, club_objid=club_objid, inclusion_objid=True)

	if my_data.get("authority") >= 2:

		logger.critical("DELETE - /api/club/delete/member : 동아리 회장만 탈퇴시킬 수 있습니다. (프론트에서 예외처리 되었을 텐데, 로그 나오면 보안상 문제있는거) !!")
		raise HTTPException(status_code=401, detail={"message": "동아리 회장만 직급을 수정할 수 있습니다."})

	# 동아리 가져오기
	club = clubs_serializer(collection_club.find({"_id": ObjectId(club_objid)}))[0]
	president = club.get("president")
	executive = club.get("executive")
	member = club.get("member")

	remove_element(president, user_objid)
	remove_element(executive, user_objid)
	remove_element(member, user_objid)

	collection_club.update_one({"_id": ObjectId(club_objid)}, {"$set": { "president": president,
																		 "executive": executive,
																		 "member": member}})
	collection_user.update_one({"_id": ObjectId(user_objid)}, {"$pull": {"clubs": club_objid}})

	logger.info(f"DELETE - /api/club/delete/member : {club.get('title')}에서 {my_data.get('user').get('realname')}({user_objid}) 유저가 탈퇴 처리됨")

	return {"message": "탈퇴 완료"}

@router.post("/api/club/post/member")
def post_club_member(club_objid: str, user_objid: str, unique_id = Depends(verify_common_token_and_get_unique_id)):
	my_data = verify_club_authority(unique_id=unique_id, club_objid=club_objid, inclusion_objid=True)

	if my_data.get("authority") >= 3:

		logger.critical("POST - /api/club/post/member : 동아리 임원 이상만 추가시킬 수 있습니다. (프론트에서 예외처리 되었을 텐데, 로그 나오면 보안상 문제있는거) !!")
		raise HTTPException(status_code=401, detail={"message": "동아리 임원 이상만 직급을 수정할 수 있습니다."})

	# 동아리 가져오기
	club = clubs_serializer(collection_club.find({"_id": ObjectId(club_objid)}))[0]
	president = club.get("president")
	executive = club.get("executive")
	member = club.get("member")

	if user_objid in member:
		raise HTTPException(status_code=400, detail={"message": "이미 가입된 사용자입니다."})
	
	# 동아리에 넣기
	collection_club.update_one({"_id": ObjectId(club_objid)}, {"$push": {"member": user_objid}})
	collection_user.update_one({"_id": ObjectId(user_objid)}, {"$push": {"clubs": club_objid}})

	logger.info(f"POST - /api/club/post/member : {club.get('title')} 동아리에 {my_data.get('user').get('realname')}({user_objid}) 유저가 가입되었습니다.")

	return {'message': "동아리에 추가 성공"}