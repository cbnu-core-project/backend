from config.database import collection_user, collection_club
from schemas.others_schema import others_serializer
from bson import ObjectId


"""
executive(임원) 이상(어드민, 회장, 임원, 동아리원)인지 권한을 확인하는 함수
0: 어드민
1: 회장
2: 임원
3: 동아리원
4: 비동아리원
"""
def verify_club_authority(unique_id: str, club_objid: str):
	user = others_serializer(collection_user.find({"unique_id": unique_id}))[0]
	club = others_serializer(collection_club.find({"_id": ObjectId(club_objid)}))[0]

	"""
	str 형식으로 바꿔줘야 제대로 == 연산자가 작동한다.
	user.get("_id") 의 타입은 ObjectId로 표현된다. ( 아마 pydantic로 바꾼 것은 출력할 때 영향을 끼치고 그 전에는 objid인 것 같다 )
	"""

	if user.get("admin"):
		return 0

	if str(user.get("_id")) in club.get("president"):
		return 1

	if str(user.get("_id")) in club.get("executive"):
		return 2

	if str(user.get("_id")) in club.get("member"):
		return 3

	return 4