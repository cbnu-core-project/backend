from pydantic import BaseModel
from datetime import datetime

class _Question(BaseModel):
    type: int
    question: str
    answer: str
    

class ClubApplicationSubmit(BaseModel):
    title: str
    content: str
    club_objid: str
    user_objid: str
    club_name:str
    deadline: datetime
    announcement_of_acceptance: datetime

 
    realname: str
    department: str
    school_number: str
    
    gender: str
    phone_number: str
    email: str
    address: str

    # 질문 리스트
    questions: list[_Question]


