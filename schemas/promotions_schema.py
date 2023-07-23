
def promotion_serializer(promotion) -> dict:
    return {
        "_id": promotion["_id"],
		"title": promotion["title"],
		"author": promotion["author"],
		"user_id": promotion["user_id"],
		"club_name": promotion["club_name"],
		"image_url": promotion["image_url"],
		"classification": promotion["classification"]
    }

def promotions_serializer(promotions) -> list:
	return [promotion_serializer(promotion) for promotion in promotions]


