import string
import random
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import time
from fastapi import HTTPException

################################
# .env 환경변수 설정
from dotenv import load_dotenv, find_dotenv
import os
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
################################
# s3 연결 및 기본 변수 세팅
import boto3

from botocore.exceptions import ClientError

s3 = boto3.client('s3',
                  aws_access_key_id = os.environ.get('IAM_ACCESS_KEY'),
                  aws_secret_access_key = os.environ.get('IAM_SECRET_ACCESS_KEY'),
                  )

BUCKET_NAME = 'core-server-bucket'

KB = 1024
MB = 1024 * KB

# 아직 안 정함
SUPPORTED_IMAGE_TYPES = [
    'image/png',
    'image/jpg',
    'image/jpeg',
    'image/gif',
]
################################


router = APIRouter(
    tags=['files']
)


@router.get('/get/files')
def get_files():
    res = s3.list_objects_v2(Bucket=BUCKET_NAME)
    return res

# 이미지 업로드
@router.post("/upload/image")
async def upload_image_file_s3(image_file: UploadFile = File(...)):
    if not image_file:
        raise HTTPException(status_code=400, detail={ "messsage": "올릴 파일이 없습니다."})

    if image_file.content_type not in SUPPORTED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail={"message": '지원하지 않는 이미지 타입입니다. jpg,jpeg,png,gif만 가능합니다.'})

    if not 0 < image_file.size <= 10 * MB:
        raise HTTPException(status_code=400, detail={"message": '10MB 이하의 이미지만 올릴 수 있습니다.'})

    # 1. 이미지 업로드용 타입 검증 필요
    # 2. 이미지 업로드 할 때 타입에 맞게 content-type 커스텀 필요 s3 메타데이터 설정 참고해서 다운로드용.. 보기용 등.. 공부

    ############################
    # 중복을 피하기 위한 랜덤 문자열 생성
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    now = time.time()

    new = f'_{rand_str}_{now}.'
    filename = new.join(image_file.filename.rsplit('.', 1))
    ############################

    try:
        print(time.time())
        s3.upload_fileobj(image_file.file, BUCKET_NAME, filename, ExtraArgs = {'ContentType': image_file.content_type})
        print(time.time())

        return { 'image_url': f"https://core-server-bucket.s3.ap-northeast-2.amazonaws.com/{filename}", 'filename': filename }
    except ClientError as err:
        raise HTTPException(status_code=500, detail={"message": err})

# 파일 업로드
@router.post("/upload/file")
async def upload_file_s3(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail={ "messsage": "올릴 파일이 없습니다."})

    if not 0 < file.size <= 10 * MB:
        raise HTTPException(status_code=400, detail={"message": '10MB 이하의 파일만 올릴 수 있습니다.'})


    ############################
    # 중복을 피하기 위한 랜덤 문자열 생성
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    now = time.time()

    new = f'_{rand_str}_{now}.'
    filename = new.join(file.filename.rsplit('.', 1))
    ############################

    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, filename, ExtraArgs = {'ContentType': file.content_type, "ContentDisposition": "attachment;"})
        return { 'file_url': f"https://core-server-bucket.s3.ap-northeast-2.amazonaws.com/{filename}", 'filename': filename}
    except ClientError as err:
        raise HTTPException(status_code=500, detail={"message": err})



# 파일 다운로드, attachement로 다운로드
@router.get('/download/files/{file_name}')
async def download(file_name: str):
    try:
        contents = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)
    except ClientError as err:
        HTTPException(status_code=500, detail={"message": err})

    # 한글 깨짐 문제로, 인코딩타입을 지정해서 보내줘야한다.
    return StreamingResponse(
        content=contents.get('Body'),
        media_type=contents.get("ContentType"),
        headers={
            "Content-Disposition": f"attachment; filename*=\"UTF-8\"{file_name.encode('utf-8')}",
        }
    )





"""
@router.post('/image')
def upload_image(image: UploadFile = File(...)):
  letter = string.ascii_letters
  rand_str = ''.join(random.choice(letter) for i in range(6))
  now = time.time()

  new = f'_{rand_str}_{now}.'
  filename = new.join(image.filename.rsplit('.', 1))
  path = f'images/{filename}'

  print(filename)

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(image.file, buffer)

  return {'image_url': path}
"""


"""
@router.post('/file')
def upload_file(file: UploadFile = File(...)):
  letter = string.ascii_letters
  rand_str = ''.join(random.choice(letter) for i in range(6))
  now = time.time()

  new = f'_{rand_str}_{now}.'
  filename = new.join(file.filename.rsplit('.', 1))
  path = f'files/{filename}'

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(file.file, buffer)

  return {'file_url': path}
  
"""