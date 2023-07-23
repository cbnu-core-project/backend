from pydantic import BaseModel
from typing import List, Union

class Faq(BaseModel):
    question : str
    answer : str
    
class ClubFaq(BaseModel):
    club_objid : str
    open_url : str
    faqs: list[Faq]
    

