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