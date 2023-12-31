import requests
import typing as t

from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from starlette import status

# .env 환경변수 설정
from dotenv import load_dotenv, find_dotenv
import os
dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

# 토큰을 swagger 문서에서 테스트 하기 위한 코드
get_bearer_token = HTTPBearer(auto_error=False)


KAKAO_REST_API_KEY = os.environ.get('KAKAO_REST_API_KEY')
KAKAO_REDIRECT_URI_PRODUCTION = os.environ.get('KAKAO_REDIRECT_URI_PRODUCTION')
KAKAO_REDIRECT_URI_DEVELOPMENT = os.environ.get('KAKAO_REDIRECT_URI_DEVELOPMENT')
KAKAO_GET_TOKEN_URL = f"https://kauth.kakao.com/oauth/token?grant_type=refresh_token&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI_PRODUCTION}&refresh_token="
KAKAO_GET_TOKEN_URL = f"https://kauth.kakao.com/oauth/token?grant_type=refresh_token&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI_PRODUCTION}&refresh_token="
KAKAO_USERINFO_URL = 'https://kapi.kakao.com/v2/user/me'
KAKAO_LOGOUT_URL = 'https://kapi.kakao.com/v1/user/logout'

NAVER_CLIENT_ID = os.environ.get('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.environ.get('NAVER_CLIENT_SECRET')
NAVER_REDIRECT_URI_PRODUCTION = os.environ.get('NAVER_REDIRECT_URI_PRODUCTION')
NAVER_REDIRECT_URI_DEVELOPMENT = os.environ.get('NAVER_REDIRECT_URI_DEVELOPMENT')
NAVER_GET_TOKEN_URL = f"https://nid.naver.com/oauth2.0/token?grant_type=refresh_token&client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&refresh_token="
NAVER_USERINFO_URL = "https://openapi.naver.com/v1/nid/me"
NAVER_DELETE_TOKEN_URL = f"https://nid.naver.com/oauth2.0/token?grant_type=delete&client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&service_provider=NAVER&access_token="




def verify_common_token_and_get_unique_id(
    auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:

    # 토큰 자체가 없다면 401
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "토큰이 존재하지 않습니다."},
        )

    token = auth.credentials
    headers = {'Authorization': 'Bearer ' + token}

    # 토큰 검증 (1. 카카오)
    response = requests.get(KAKAO_USERINFO_URL, headers=headers)
    if response.ok:
        id = response.json().get('id')
        return f"kakao_{id}"

    # 토큰 검증 (2. 네이버)
    response = requests.get(NAVER_USERINFO_URL, headers=headers)
    if response.ok:
        id = response.json().get('response').get('id')
        return f"naver_{id}"

    # 토큰이 유효하지 않다면 401
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"message": "토큰이 유효하지 않습니다."},
    )


def verify_common_refresh_token_and_create_access_token(refresh_token):
    # refresh_token을 이용한 access_token 재발급
    if refresh_token == None:
        raise HTTPException(status_code=401, detail={"message": "토큰이 없습니다."})

    # 토큰 검증 (1. 카카오)
    kakao_headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    response = requests.get(KAKAO_GET_TOKEN_URL +
                            refresh_token, headers=kakao_headers)
    if response.ok:
        new_kakao_access_token = response.json().get('access_token')
        print(response.json().get('expires_in'))
        if new_kakao_access_token != None:
            return new_kakao_access_token

    # 토큰 검증 (2. 네이버)
    response = requests.get(NAVER_GET_TOKEN_URL + refresh_token)
    if response.ok:
        new_naver_access_token = response.json().get('access_token')
        print(response.json().get('expires_in'))
        if new_naver_access_token != None:
            return new_naver_access_token

    # 토큰이 유효하지 않다면 401
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"message": "토큰이 유효하지 않습니다."},
    )

# 헤더를 통해 읽어와서 로그아웃 (Depend)


def common_header_access_token_logout(auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)):
    token = auth.credentials
    headers = {'Authorization': 'Bearer ' + token}

    # 1. 카카오 로그아웃
    response = requests.post(KAKAO_LOGOUT_URL, headers=headers)

    # 2. 네이버 로그아웃
    response = requests.post(NAVER_DELETE_TOKEN_URL + token)

    return {"message": "access_token 만료 처리"}

# 파라미터로 받아서 로그아웃


def common_access_token_logout(access_token: str):
    headers = {'Authorization': 'Bearer ' + access_token}

    # 1. 카카오 로그아웃
    response = requests.post(KAKAO_LOGOUT_URL, headers=headers)

    # 2. 네이버 로그아웃
    response = requests.post(NAVER_DELETE_TOKEN_URL + access_token)

    return {"message": "access_token 만료 처리"}
