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
        # collection_notice.update_one({"_id": notice.get("_id")}, { "$rename": {"author": 'nickname'}})
        # collection_notice.update_one({"_id": notice.get("_id")}, { "$set": {"last_updated": ''}})
        collection_notice.update_one({"_id": notice.get("_id")}, { "$currentDate": {"last_updated": True}})

def club_migrate():
    collection_club.update_many({}, {"$set": { "main_content": ""}})
    collection_club.update_many({}, {"$rename": { "content": "sub_content"}})
    # collection_club.update_many({}, {"$currentDate": { "last_updated": True}})

def users_migrate():
    collection_user.update_many({}, {"$set": {"interests": []}})
    
def club_application_submit_migrate():
    collection_club_application_submit.update_one({},{"$set": {"user_objid": ""}})

def schedule_migrate():
    collection_schedule.update_many({}, {"$set": {"users": ["64ba1a1fd2d5e9671f8e07bc", "64be3b2d8f83d5c67de006e7", "64c22f6cd3a8a5f2797449b4" ]}})

if __name__ == "__main__":
    schedule_migrate()

