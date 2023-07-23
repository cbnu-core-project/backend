from bson.json_util import loads, dumps

"""
이 부분은 앞으로 수정이 여러번 될 예정이고, 귀찮으므로..
schedule 부분만 예외적으로 loads(dumps()) 사용
"""
def schedules_serializer(schedules) -> list:
	datas = loads(dumps(schedules))
	return datas
