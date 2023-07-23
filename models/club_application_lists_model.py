from pydantic import BaseModel

class ClubApplicationList(BaseModel):
    realname: str
    content: str
    club_objid: str
    club_name: str
    user_objid: str
    username: str
    approval: int # 0 : 합격, 1 : 대기, 2 : 불합격
    image_urls: list[str]
    classification: int