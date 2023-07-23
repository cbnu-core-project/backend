import requests
import typing as t

from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from starlette import status

# We will handle a missing token ourselves
get_bearer_token = HTTPBearer(auto_error=False)

NAVER_USERINFO_URL = "https://openapi.naver.com/v1/nid/me"


class UnauthorizedMessage(BaseModel):
	detail: str = "유효하지 않는 토큰이다."



# We will handle a missing token ourselves
get_bearer_token = HTTPBearer(auto_error=False)

class UnauthorizedMessage(BaseModel):
	detail: str = "유효하지 않는 토큰이다."

async def verify_and_get_naver_token(
    auth: t.Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
	print(auth)
	token = auth.credentials
	headers = {'Authorization': 'Bearer ' + token }
	response = requests.get(NAVER_USERINFO_URL, headers=headers)

	if auth is None or not(response.ok):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=UnauthorizedMessage().detail,
		)
	return token