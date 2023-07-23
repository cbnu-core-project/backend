from pydantic import BaseModel
from datetime import datetime


class Notice(BaseModel):
	title: str
	content: str
	user_objid: str
	nickname: str
	last_updated: datetime | None = None
