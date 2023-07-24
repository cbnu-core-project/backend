from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# 라우터
from routers import clubs, notices, promotions, files, schedules, club_active_records, club_activity_history, club_programs,users, club_application_form, club_faq, club_application_submit,club_application_lists
from routers.oauth import kakao_oauth, naver_oauth



app = FastAPI()

##########################################################
# CORS 설정 #
origins = ["http://localhost:3000", "*"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)
##########################################################

@app.get("/")
async def home():
	return {"message": "hello world !"}

# 이미지/파일 staticFiles 마운트
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount('/files', StaticFiles(directory='files'), name='files')

# 라우터 사용 설정
app.include_router(clubs.router)
app.include_router(notices.router)
app.include_router(promotions.router)
app.include_router(files.router)
app.include_router(schedules.router)
app.include_router(club_active_records.router)
app.include_router(kakao_oauth.router)
app.include_router(naver_oauth.router)
app.include_router(users.router)
app.include_router(club_activity_history.router)
app.include_router(club_programs.router)
app.include_router(club_faq.router)
app.include_router(club_application_lists.router)
app.include_router(club_application_form.router)
app.include_router(club_application_submit.router)



