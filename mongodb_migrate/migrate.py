from config.database import collection_club, collection_notice, collection_user, collection_schedule, collection_club_application_submit
from schemas.clubs_schema import clubs_serializer
from schemas.users_schema import users_serializer
from schemas.others_schema import others_serializer

def club_image_url_conversion():
    # collection_club.update_many({}, {"$rename": {"image_url": "image_urls"}})
    clubs = clubs_serializer(collection_club.find())
    for club in clubs:
        image = club.get("image_urls")
        collection_club.update_one({"_id": club.get("_id")}, {'$set':{"image_urls": [image]}})

def notice_conversion():
    notices = others_serializer(collection_notice.find())
    for notice in notices:
        # collection_notice.update_one({"_id": notice.get("_id")}, { "$unset": {"club_name": ''}})
        # collection_notice.update_one({"_id": notice.get("_id")}, { "$rename": {"user_id": 'user_objid'}})
        collection_notice.update_one({"_id": notice.get("_id")}, { "$rename": {"nickname": 'realname'}})
        # collection_notice.update_one({"_id": notice.get("_id")}, { "$set": {"last_updated": ''}})
        # collection_notice.update_one({"_id": notice.get("_id")}, { "$currentDate": {"last_updated": True}})

def club_migrate():
    collection_club.update_many({}, {"$set": { "president": []}})
    collection_club.update_many({}, {"$set": { "executive": []}})
    collection_club.update_many({}, {"$set": { "member": []}})
    # collection_club.update_many({}, {"$rename": { "content": "sub_content"}})
    # collection_club.update_many({}, {"$currentDate": { "last_updated": True}})

def users_migrate():
    collection_user.update_many({}, {"$rename": {"adress": "address"}})
    # collection_user.update_many({}, {"$set": {"gender": "male"}})

def club_application_submit_migrate():
    collection_club_application_submit.update_one({},{"$set": {"user_objid": ""}})

def schedule_migrate():
    # collection_schedule.update_many({}, {"$set": {"color": "red"}})
    # collection_schedule.update_many({}, {"$set": {"users": ["64ba1a1fd2d5e9671f8e07bc", "64bb9cb3e5723a73730bfb63", "64be3b2d8f83d5c67de006e7", "64c22f6cd3a8a5f2797449b4", "64ba1f0aacc5b13be3519f1d"] }})
    collection_schedule.update_many({}, {"$set": {"content": """이 편지는 영국에서 최초로 시작되어 일년에 한 바퀴 돌면서 받는 사람에게

행운을 주었고 지금은 당신에게로 옮겨진 이 편지는 4일 안에 당신 곁을 떠나야 합니다.

이 편지를 포함해서 7통을 행운이 필요한 사람에게 보내 주셔야 합니다.

복사를 해도 좋습니다. 혹 미신이라 하실지 모르지만 사실입니다.

영국에서 HGXWCH이라는 사람은 1930년에 이 편지를 받았습니다. 그는 비서에게 복사해서 보내라고 했습니다.

며칠 뒤에 복권이 당첨되어 20억을 받았습니다. 어떤 이는 이 편지를 받았으나

96시간 이내 자신의 손에서 떠나야 한다는 사실을 잊었습니다. 그는 곧 사직되었습니다.

나중에야 이 사실을 알고 7통의 편지를 보냈는데 다시 좋은 직장을 얻었습니다.

미국의 케네디 대통령은 이 편지를 받았지만 그냥 버렸습니다. 결국 9일 후 그는 암살 당했습니다.

기억해 주세요. 이 편지를 보내면 7년의 행운이 있을 것이고 그렇지 않으면 3년의 불행이 있을 것입니다.

그리고 이 편지를 버리거나 낙서를 해서는 절대로 안됩니다. 7통입니다.

이 편지를 받은 사람은 행운이 깃들 것입니다. 힘들겠지만 좋은게 좋다고 생각하세요. 7년의 행운을 빌면서.."""}})

if __name__ == "__main__":
    notice_conversion()

