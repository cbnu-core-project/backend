from config.database import collection_club, collection_notice
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



if __name__ == "__main__":
    pass
