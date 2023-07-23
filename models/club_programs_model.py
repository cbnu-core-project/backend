from pydantic import BaseModel

class ClubPrograms(BaseModel):
    title: str
    content: str
    club_objid: str
