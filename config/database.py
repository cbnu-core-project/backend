import pymongo
from bson import ObjectId
import certifi
from pydantic.json import ENCODERS_BY_TYPE

# .env 환경변수 설정
from dotenv import load_dotenv, find_dotenv
import os
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

# mongodb 보안에러 해결을 위한 패키지
ca = certifi.where()

################################################################
ENCODERS_BY_TYPE[ObjectId] = str

client = pymongo.MongoClient(
	os.environ.get("MONGODB_URI"),
	tlsCAFile=ca
)

db = client['core_data']

collection_club = db['club']
collection_promotion = db['promotion']
collection_notice = db['notice']
collection_user = db['user']
collection_schedule = db['schedule']
collection_club_active_record = db['club_active_record']
collection_club_application_list = db['club_application_list']
collection_club_faq = db['club_faq']
collection_club_activity_history = db['club_activity_history']
collection_club_programs = db['club_program']
collection_club_faq = db['club_faq']
collection_club_application_form = db['club_application_form']
################################################################