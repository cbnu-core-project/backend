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


@router.get('/download/file/{file_name}', response_class=FileResponse)
def download(file_name: str):
    path = f"files/{file_name}"
    return path