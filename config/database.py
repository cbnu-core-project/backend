import pymongo
from bson import ObjectId
import certifi
from pydantic.json import ENCODERS_BY_TYPE

################################################################
ENCODERS_BY_TYPE[ObjectId] = str


# mongodb 보안에러 해결을 위한 패키지
ca = certifi.where()

client = pymongo.MongoClient(
	"mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority",
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