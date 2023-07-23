import requests
import typing as t

from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from starlette import status


# We will handle a missing token ourselves
get_bearer_token = HTTPBearer(auto_error=False)

KAKAO_USERINFO_URL = 'https://kapi.kakao.com/v2/user/me'
NAVER_USERINFO_URL = "https://openapi.naver.com/v1/nid/me"

class UnauthorizedMessage(BaseModel):
	detail: str = "유효하지 않는 토큰이다."

def verify_common_token_and_get_unique_id(
    auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
    # 토큰 자체가 없다면 401
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )

    token = auth.credentials
    headers = {'Authorization': 'Bearer ' + token }

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
            detail=UnauthorizedMessage().detail,
        )

KAKAO_REST_API_KEY = "40d478c8d7447b20143b402959fd7ed8";
KAKAO_REDIRECT_URI = "http://localhost:3000";
KAKAO_GET_TOKEN_URL = f"https://kauth.kakao.com/oauth/token?grant_type=refresh_token&client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&refresh_token="

NAVER_CLIENT_ID = "zB5gfqdBq1a0jq6vr_zv";
NAVER_CLIENT_SECRET = "X8C0M1JHIH"
NAVER_REDIRECT_URI = "http://localhost:3000";
NAVER_GET_TOKEN_URL = f"https://nid.naver.com/oauth2.0/token?grant_type=refresh_token&client_id={NAVER_CLIENT_ID}&client_secret={NAVER_CLIENT_SECRET}&refresh_token="


def verify_common_refresh_token_and_create_access_token(refresh_token):
    # refresh_token을 이용한 access_token 재발급


    # 토큰 검증 (1. 카카오)
    kakao_headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    response = requests.get(KAKAO_GET_TOKEN_URL + refresh_token, headers=kakao_headers)
    if response.ok:
        new_kakao_access_token = response.json().get('access_token')
        print(response.json().get('expires_in'))
        return new_kakao_access_token

    # 토큰 검증 (2. 네이버)
    response = requests.get(NAVER_GET_TOKEN_URL + refresh_token)
    if response.ok:
        new_naver_access_token = response.json().get('access_token')
        print(response.json().get('expires_in'))
        return new_naver_access_token

    # 토큰이 유효하지 않다면 401
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )