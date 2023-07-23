from pydantic import BaseModel


class Promotion(BaseModel):
	title: str
	content: str
	author: str
	user_id: str
	club_name: str
	image_url: str
	classification: int
