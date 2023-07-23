def notice_serializer(notice) -> dict:
    return {
        "_id": notice["_id"],
		"title": notice["title"],
		"content": notice["content"],
		"author": notice["author"],
		"user_id": notice["user_id"],
		"club_name": notice["club_name"],
		"classification": notice["classification"]
    }

def notices_serializer(notices) -> list:
	return [notice_serializer(notice) for notice in notices]