from pydantic import BaseModel

class ClubFaq(BaseModel):
    club_objid : str
    quest : str
    answer : str

class ClubFaqOpenURL(BaseModel):
    club_objid : str
    open_url : str
    
 