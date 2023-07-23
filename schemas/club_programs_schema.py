#동아리 소개 - 동아리 프로그램 DB Schema
def club_program_serializer(club_program) -> dict:
    return {
        "_id": club_program["_id"],
		"title": club_program["title"],
		"content": club_program["content"],
        "club_objid": club_program["club_objid"],
    }

def club_programs_serializer(club_programs) -> list:
	return [club_program_serializer(club_program) for club_program in club_programs]