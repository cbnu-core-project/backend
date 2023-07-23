from bson import ObjectId
from fastapi import APIRouter
from config.database import collection_promotion
from models.promotions_model import Promotion
from schemas.promotions_schema import promotions_serializer

router = APIRouter(
	tags=["promotions"]
)

@router.get("/api/promotions", description="홍보글 전체 가져오기")
async def read_all_promotion():
	promotions = promotions_serializer(collection_promotion.find())

	return promotions


@router.get("/api/promotions/classification/", description="홍보글 분류별 전체 가져오기")
async def read_all_promotion(classification: int):
	promotions = promotions_serializer(collection_promotion.find({"classification": classification}))

	return promotions


@router.get("/api/promotion/{objid}", description="오브젝트아이디에 맞는 홍보글 1개만 가져오기(리스트로 받아옴)")
async def read_one_promotion(objid: str):
	promotion = promotions_serializer(collection_promotion.find({"_id": ObjectId(objid)}))

	return promotion


@router.get("/api/promotions/some/", description="홍보글 skip, limit를 통한 동아리 일부 가져오기\nex) 3번째부터 4개 가져오려면, -> skip=2, limit=4")
async def read_some_promotion(skip: int, limit: int):
	promotions = promotions_serializer(collection_promotion.find().skip(skip).limit(limit))

	return promotions


@router.get("/api/promotions/some/classification/", description="홍보글 skip, limit를 통한 글 일부 가져오기\n그리고 classification을 통한 중앙 동아리 직무 동아리 구분 가능")
async def read_some_promotion(skip: int, limit: int, classification: int):
	promotions = promotions_serializer(collection_promotion.find({"classification": classification}).skip(skip).limit(limit))

	return promotions

@router.get("/api/promotions/search/", description="검색어 쿼리로 넘기기")
async def search_promotion(query: str):
	condition = [
  {
    '$search': {
      'index': "promotionSearch",
      'text': {
        'query': query,
        'path': ['title', 'content']
      }
    }
  },
		{ '$addFields': { 'score' : { '$meta': 'searchScore'}}}
]

	promotions = promotions_serializer(collection_promotion.aggregate(condition))

	return promotions


@router.get("/api/promotions/search/classification/", description="검색어 및 분류 쿼리로 넘기기")
async def search_promotion(query: str, classification: int):
	condition = [
  	{
    '$search': {
      'index': "promotionSearch",
      'text': {
        'query': query,
        'path': ['title', 'content']
      		}
    	}
  	},
	{'$match': {'classification': classification}},
	{ '$addFields': { 'score' : { '$meta': 'searchScore'}}}
]

	promotions = promotions_serializer(collection_promotion.aggregate(condition))

	return promotions



@router.post("/api/promotion", description="홍보글 추가하기 / classification = 1 -> 중앙동아리, 2 -> 직무동아리")
async def create_promotion(promotion: Promotion):
	_id = collection_promotion.insert_one(dict(promotion))
	promotion = promotions_serializer(collection_promotion.find({"_id": _id.inserted_id}))

	return promotion


@router.delete("/api/promotion/{objid}", description="홍보글 삭제하기 - ex) /api/post/123412 (삭제할 objectid) 경로로 'delete' 요청")
async def delete_promotion(objid: str):
	collection_promotion.delete_one({"_id": ObjectId(objid)})
	return []