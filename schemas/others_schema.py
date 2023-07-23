from bson.json_util import loads, dumps

"""
앞으로 수정이 여러번 될 예정이고, 귀찮으므로..
예외적으로 loads(dumps()) 사용
"""
def others_serializer(others) -> list:
	datas = loads(dumps(others))
	return datas
