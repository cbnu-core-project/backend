from pydantic import BaseModel

class ClubApplicationList(BaseModel):
    user_objid: str
    club_objid: str
    title: str
    club_name: str
    approval: int # 0 : 합격, 1 : 대기, 2 : 불합격
    classification: int
    data: dict
    



