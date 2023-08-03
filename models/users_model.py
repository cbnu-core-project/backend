from pydantic import BaseModel


class User(BaseModel):
    email: str
    realname: str
    nickname: str
    profile_image_url: str
    clubs: list[str] # 속해있는 동아리
    major: str
    student_number: str
    phone_number: str
    interests: list[str] #관심있는 동아리
    ################################################################
    # unique_id: str
    # social: str
    # refresh_token: str
    # admin: bool





