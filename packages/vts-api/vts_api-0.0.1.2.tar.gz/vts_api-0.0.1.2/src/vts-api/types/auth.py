from .base import BaseRequest, BaseResponse
from .error import APIError

from .data import AuthenticationResponseData, AuthenticationRequestData, \
	AuthenticationTokenRequestData, AuthenticationTokenResponseData


class AuthenticationTokenRequest(BaseRequest):
	data: AuthenticationTokenRequestData


class AuthenticationTokenResponse(BaseResponse):
	data: AuthenticationTokenResponseData | APIError


class AuthenticationRequest(BaseRequest):
	data: AuthenticationRequestData


class AuthenticationResponse(BaseResponse):
	data: AuthenticationResponseData
