import string
import random
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import time


router = APIRouter(
    tags=['files']
)

# @router.post('/uploadimage')
# def get_uploadfile(upload_file: UploadFile = File(...)):
#     filename = upload_file.filename
#
#     path = f"images/{filename}"
#     with open(path, 'w+b') as buffer:
#         shutil.copyfileobj(upload_file.file, buffer)
#
#     return {
#         'filename': path,
#         'type': upload_file.content_type
#     }

@router.post('/image')
def upload_image(image: UploadFile = File(...)):
  letter = string.ascii_letters
  rand_str = ''.join(random.choice(letter) for i in range(6))
  now = time.time()

  new = f'_{rand_str}_{now}.'
  filename = new.join(image.filename.rsplit('.', 1))
  path = f'images/{filename}'

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(image.file, buffer)

  return {'image_url': path}

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


# 파일 다운로드, attachement로 다운로드
@router.get('/download/files/{file_name}')
def download(file_name: str):
    file_path = f"files/{file_name}"

    # 난수가 들어가기 전의 기존 파일이름 구하기
    # file_type = file_name.split('.')[-1]
    # origin_file_name = '_'.join(file_name.split('.')[0].split('_')[0:-2]) + '.' + file_type
    # print(origin_file_name)
    # print(file_name.split('.')[0].split('_')[0:-2])

    # print(file_name.encode('utf-8').decode('utf-8'))

    # 한글 깨짐 문제로, 인코딩타입을 지정해서 보내줘야한다.
    response = FileResponse(file_path, headers={
        "Content-Disposition": f"attachment; filename*=\"UTF-8\"{file_name.encode('utf-8')}",
    })
    return response