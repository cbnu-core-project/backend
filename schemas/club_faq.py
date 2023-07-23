#동아리 소개 - 동아리 활동 내역 DB Schema
def club_faq_serializer(club_faq) -> dict:
    return {
        "_id": club_faq["_id"],
		"open_url": club_faq["open_url"],
        "faqs": club_faq["faqs"],
        "club_objid": club_faq["club_objid"]
    }
    
def club_faqs_serializer(club_faqs) -> list:
	return [club_faq_serializer(club_faq) for club_faq in club_faqs]