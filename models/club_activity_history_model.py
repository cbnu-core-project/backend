from pydantic import BaseModel

class ClubActivityHistory(BaseModel):
    title: str
    year: str
    month: str
    club_objid: str
    
 