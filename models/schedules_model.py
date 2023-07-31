import datetime as datetime
from pydantic import BaseModel



class Schedule(BaseModel):
	# relative_schedule_unique_id: str # 연관된 스케줄의 unique_id 백엔드에서 만들거임
	user_objid: str
	user_unique_id: str
	realname: str
	email: str
	club_objid: str # str 타입으로 넣을거임
	club_name: str
	title: str
	content: str
	place: str
	users: list[str] # 참여하는 유저의 objid 리스트
	start_datetime: datetime.datetime # 실제 start datetime
	end_datetime: datetime.datetime
	################################################################
	calendar_start_datetime: datetime.datetime # 캘린더에 그려주기 위해 일주일 넘어가는 단위로 끊은 것
	schedule_length: int # 캘린더 start_datetime 기준 그 주의 마지막 까지의length


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


