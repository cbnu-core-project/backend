from pydantic import BaseModel


class ClubActiveRecord(BaseModel):
    title: str
    content: str
    club_objid: str
    club_name:str
    author: str
    user_id: str
    image_urls: list[str]
    classification: int