from config.database import collection_user, collection_club
from schemas.others_schema import others_serializer
from bson import ObjectId
from fastapi import HTTPException


"""
executive(임원) 이상(어드민, 회장, 임원, 동아리원)인지 권한을 확인하는 함수
0: 어드민
1: 회장
2: 임원
3: 동아리원
4: 비동아리원
"""
def verify_club_authority(unique_id: str, club_objid: str, inclusion_objid: bool = False):
	user = others_serializer(collection_user.find({"unique_id": unique_id}))[0]
	club = others_serializer(collection_club.find({"_id": ObjectId(club_objid)}))[0]

	"""
	str 형식으로 바꿔줘야 제대로 == 연산자가 작동한다.
	user.get("_id") 의 타입은 ObjectId로 표현된다. ( 아마 pydantic로 바꾼 것은 출력할 때 영향을 끼치고 그 전에는 objid인 것 같다 )
	"""

	if user.get("admin"):
		if inclusion_objid:
			return { "authority": 0, "objid": str(user.get("_id")) }
		else:
			return 0

	if str(user.get("_id")) in club.get("president"):
		if inclusion_objid:
			return { "authority": 1, "objid": str(user.get("_id")) }
		else:
			return 1

	if str(user.get("_id")) in club.get("executive"):
		if inclusion_objid:
			return { "authority": 2, "objid": str(user.get("_id")) }
		else:
			return 2

	if str(user.get("_id")) in club.get("member"):
		if inclusion_objid:
			return { "authority": 3, "objid": str(user.get("_id")) }
		else:
			return 3

	if inclusion_objid:
		return { "authority": 4, "objid": str(user.get("_id")) }
	else:
		return 4

def return_club_member_info_and_club_authority(club_objid: str):
	club = others_serializer(collection_club.find({"_id": ObjectId(club_objid)}))[0]

	user_objid_list = club.get("member")

	if len(user_objid_list) == 0:
		raise HTTPException(status_code=400,  detail={"message": "현재 동아리 멤버가 아무도 존재하지 않습니다."})

	# 검색 조건 설정
	query = {"$or": [{"_id": ObjectId(user_objid)} for user_objid in user_objid_list]}

	users = others_serializer(collection_user.find(query).sort("realname", 1))

	# user정보 리스트에 유저 권한도 끼워넣기
	for user in users:
		if user.get("admin"):
			user["current_club_authority"] = 0

		elif str(user.get("_id")) in club.get("president"):
			user["current_club_authority"] = 1

		elif str(user.get("_id")) in club.get("executive"):
			user["current_club_authority"] = 2

		elif str(user.get("_id")) in club.get("member"):
			user["current_club_authority"] = 3

		else:
			user["current_club_authority"] = 4

	return users

# 테스트용 코드
if __name__ == "__main__":
    print(return_club_member_info_and_club_authority("6460426f53f96addfe9e2c36"))
