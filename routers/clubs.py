from bson import ObjectId
from fastapi import APIRouter
from config.database import collection_club
from models.clubs_model import Club
from schemas.clubs_schema import clubs_serializer


router = APIRouter(
	tags=["clubs"]
)


@router.get("/api/clubs", description="동아리 전체 가져오기")
async def read_all_club():
	clubs = clubs_serializer(collection_club.find())

	return clubs


@router.get("/api/clubs/classification/", description="동아리 분류별 전체 가져오기")
async def read_all_club(classification: int):
	clubs = clubs_serializer(collection_club.find({"classification": classification}))

	return clubs


@router.get("/api/club/{objid}", description="오브젝트아이디에 맞는 동아리 1개만 가져오기(리스트로 받아옴)")
async def read_one_club(objid: str):
	# 비록 1개의 동아리만 가져오지만, 리스트형태로 받아온다.
	club = clubs_serializer(collection_club.find({"_id": ObjectId(objid)}))

	return club


@router.get("/api/clubs/some/", description="동아리 skip, limit를 통한 동아리 일부 가져오기\nex) 3번째부터 4개 가져오려면, -> skip=2, limit=4")
async def read_some_club(skip: int, limit: int):
	clubs = clubs_serializer(collection_club.find().skip(skip).limit(limit))

	return clubs


@router.get("/api/clubs/some/classification/", description="동아리 skip, limit를 통한 글 일부 가져오기\n그리고 classification을 통한 중앙 동아리 직무 동아리 구분 가능")
async def read_some_club(skip: int, limit: int, classification: int):
	clubs = clubs_serializer(collection_club.find({"classification": classification}).skip(skip).limit(limit))

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

	return clubs


@router.post("/api/club", description="동아리 추가하기 / classification = 0 -> 중앙동아리, 1 -> 직무동아리")
async def create_club(club: Club):
	_id = collection_club.insert_one(dict(club))
	club = clubs_serializer(collection_club.find({"_id": _id.inserted_id}))

	return club


@router.put("/api/club/{objid}", description="동아리 수정하기")
async def update_club(objid: str, club: Club):
	collection_club.update_one({"_id": ObjectId(objid)}, {"$set": dict(club)})
	club = clubs_serializer(collection_club.find({"_id": ObjectId(objid)}))

	return club

@router.delete("/api/club/{objid}", description="동아리 삭제하기 - ex) /api/post/123412 (삭제할 objectid) 경로로 'delete' 요청")
async def delete_club(objid: str):
	collection_club.delete_one({"_id": ObjectId(objid)})
	return []

@router.post("/api/club/activity_tag/push", description="동아리 활동태그 추가(push)하기")
def delete_activity_tag(objid: str, activity_tag: str):
	collection_club.update_one({"_id": ObjectId(objid)}, {"$push" : {"activity_tags": activity_tag}})
	return "추가 완료"

@router.delete("/api/club/activity_tag/index", description="동아리 활동태그 인덱스를 통해 삭제하기")
def delete_activity_tag(objid: str, index: int):

	collection_club.update_one({"_id": ObjectId(objid)}, {"$unset": {f"activity_tags.{index}": 1}})
	collection_club.update_one({"_id": ObjectId(objid)}, {"$pull": {"activity_tags": None}})

	return "태그 삭제 완료"


@router.post("/api/club/image/push", description="쿼리파라미터로, 수정할 club의 objid랑, 추가할 image_url 주기")
def push_image_url(club_objid: str, image_url: str):
	collection_club.update_one({"_id": ObjectId(club_objid)}, { "$push" : { "image_urls": image_url}})
	return "push success"

@router.put("/api/club/image/update", description="쿼리파라미터로, 수정할 club의 objid랑, 대체할 image_url 주기")
def push_image_url(club_objid: str, image_url: str):
	collection_club.update_one({"_id": ObjectId(club_objid)}, { "$set" : { "image_urls": [image_url]}})
	return "image update success"