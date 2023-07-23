from pydantic import BaseModel


class _Question(BaseModel):
    type: str
    required: bool
    question: str

class ClubApplicationForm(BaseModel):
    title: str
    content: str
    club_objid: str
    club_name:str

    # 받아들일 항목 여부 bool / 기본필수
    realname: bool
    department: bool
    school_number: bool

    # 받아들일 항목 여부 bool / 필수여부(required) bool -> [bool, bool]
    gender: list[bool]
    phone_number: list[bool]
    email: list[bool]
    address: list[bool]

    # 질문 리스트
    questions: list[_Question]


