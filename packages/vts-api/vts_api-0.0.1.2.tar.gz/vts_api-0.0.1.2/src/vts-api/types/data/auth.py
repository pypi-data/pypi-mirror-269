from pydantic import BaseModel


class AuthenticationTokenRequestData(BaseModel):
	pluginName: str
	pluginDeveloper: str
	pluginIcon: str


class AuthenticationTokenResponseData(BaseModel):
	authenticationToken: str


class AuthenticationRequestData(BaseModel):
	pluginName: str
	pluginDeveloper: str
	authenticationToken: str


class AuthenticationResponseData(BaseModel):
	authenticated: bool
	reason: str
