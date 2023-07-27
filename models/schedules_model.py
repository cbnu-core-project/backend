import datetime as datetime
from pydantic import BaseModel



class Schedule(BaseModel):
	user_objid: str
	user_unique_id: str
	realname: str
	email: str
	club_objid: str # str 타입으로 넣을거임
	club_name: str
	title: str
	content: str
	place: str
	start_datetime: datetime.datetime
	end_datetime: datetime.datetime


# class _Schedule(BaseModel):
# 	username: str
# 	realname: str
# 	club_objid: str # str 타입으로 넣을거임
# 	club_name: str
# 	title: str
# 	content: str
# 	place: str
# 	# datetime: datetime.datetime
# 	year: str # 년
# 	month: str # 월
# 	date: str # 일
# 	day: str # 요일
# 	start_hour: str
# 	start_minute: str
# 	# start_second: str
# 	end_hour: str
# 	end_minute: str


