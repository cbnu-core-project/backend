from pydantic import BaseModel
from datetime import datetime

class Club(BaseModel):
	title: str
	main_content: str
	sub_content: str
	user_objid: str
	image_urls: list[str]
	activity_tags: list[str]
	nickname: str
	tag1: str
	tag2: str
	tag3: str
	classification: int
	last_updated: datetime | None = None

	# 권한 회장/임원/일반
	president: list[str]
	executive: list[str]
	member: list[str]
