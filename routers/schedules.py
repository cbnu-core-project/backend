from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from schemas.schedules_schema import schedules_serializer
from schemas.others_schema import others_serializer
from config.database import collection_schedule, collection_user
from models.schedules_model import Schedule
from utils.common_token import verify_common_token_and_get_unique_id
from pydantic import BaseModel
from utils.authority import verify_club_authority
import string
import random
import time
import pendulum
from datetime import datetime

router = APIRouter(
    tags=["schedules"]
)

"""
생각해보니 동아리 별 권한이 필요하다.
그래서 db구조를 다시 짜야 할 것 같다. 동아리 별 권한이라.. 좀 까다롭다.
동아리마다 관리자, 임원 리스트를 두고 검증해야겠다..
단순히 숫자로 검증하는 것이 아닐 것 같다.
"""
# 스케줄 관리 권한 확인 ( 수정, 추가, 삭제 ) ( 읽기 x )
# def verify_schedule_management_authority(club_objid, user):
#     # 현재 속해 있는 클럽(동아리)와 data(post, schedule)추가/수정 대상의 동아리 비교
#     if not(club_objid in user.get("clubs")):
#         raise HTTPException(status_code=400, detail="속해있는 동아리가 아닙니다.")
#     return True
#     # if user.get("authority") <= 2:
#     #     return user



@router.get('/api/user/schedule', description="날짜(start_datetime) 순서대로 정렬해서 데이터를 가져옴")
def get_user_schedule(unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    user = others_serializer(collection_user.find({"unique_id": unique_id}))[0]
    # 토큰이 유효하면 밑에 실행
    clubs = user.get('clubs')

    # 검색 조건 설정
    query = {"$or": [{"club_objid": club} for club in clubs]}

    # 검색하기
    results = schedules_serializer(collection_schedule.find(query).sort("start_datetime", 1))

    return results


@router.get('/api/user/schedule/club_objid/{club_objid}', description="동아리별 날짜(start_datetime) 순서대로 정렬해서 데이터를 가져옴")
def get_user_schedule(club_objid: str):

    # 검색 조건 설정
    query = {"club_objid": club_objid}

    # 검색하기
    results = schedules_serializer(collection_schedule.find(query).sort("start_datetime", 1))

    return results

@router.post('/api/user/schedule')
def create_user_schedule(schedule: Schedule, unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    # unique_id 난수를 통해 생성
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    now = time.time()
    relative_schedule_unique_id = f'{rand_str}_{now}'


    schedule_dict = dict(schedule)
    schedule_dict["relative_schedule_unique_id"] = relative_schedule_unique_id
    club_objid = schedule_dict.get('club_objid')

    # 토큰이 유효하고, 동아리 권한이 2이하라면(임원이상)
    authority = verify_club_authority(unique_id, club_objid)
    if authority > 2:
        raise HTTPException(status_code=401, detail={"message": "임원이상의 권한이 필요합니다.", "authority": authority})

    start = pendulum.instance(schedule.start_datetime)
    if (start.day_of_week == 0):
        start_week_sunday = start
    else:
        start_week_sunday = start.start_of('week').subtract(days=1)
    print(start_week_sunday)

    # start.month 와 start.day 를 반복하며.. 일요일 로 끊어준다?


    # collection_schedule.insert_one(schedule_dict)

    return { "message": "추가 성공", "authority": authority}

# 받아온 schedule 데이터로 전부 대체
# @router.put('/api/user/schedule/{objid}')
# def update_user_schedule(objid: str, schedule: Schedule, unique_id: str = Depends(verify_common_token_and_get_unique_id)):
#     schedule_dict = dict(schedule)
#     club_objid = schedule_dict.get('club_objid')
#
#     # 토큰이 유효하고, 동아리 권한이 2이하라면(임원이상)
#     authority = verify_club_authority(unique_id, club_objid)
#     if authority > 2:
#         raise HTTPException(status_code=401, detail={"message": "임원이상의 권한이 필요합니다.", "authority": authority})
#
#     collection_schedule.update_one({"_id": ObjectId(objid)}, {"$set": schedule_dict})
#
#     return {"message": "수정 성공", "authority": authority}

@router.delete('/api/user/schedule/{schedule_objid}')
def delete_user_schedule(schedule_objid: str, unique_id: str = Depends(verify_common_token_and_get_unique_id)):
    try:
        schedule = schedules_serializer(collection_schedule.find({"_id": ObjectId(schedule_objid)}))
        club_objid = schedule[0].get("club_objid")
    except:
        raise HTTPException(status_code=400, detail={"message": "유효하지 않은 objid"})

    # 토큰이 유효하고, 동아리 권한이 2이하라면(임원이상)
    authority = verify_club_authority(unique_id, club_objid)
    if authority > 2:
        raise HTTPException(status_code=401, detail={"message": "임원이상의 권한이 필요합니다.", "authority": authority})

    collection_schedule.delete_one({"_id": ObjectId(schedule_objid)})
    return {"message": "삭제 성공", "authority": authority}



