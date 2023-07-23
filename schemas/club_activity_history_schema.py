#동아리 소개 - 동아리 활동 내역 DB Schema
def club_activity_history_serializer(club_activity_history) -> dict:
    return {
        "_id": club_activity_history["_id"],
		"year": club_activity_history["year"],
		"month": club_activity_history["month"],
        "title": club_activity_history["title"],
        "club_objid": club_activity_history["club_objid"],
    }

def club_activities_history_serializer(club_activities_history) -> list:
	return [club_activity_history_serializer(club_activity_history) for club_activity_history in club_activities_history]