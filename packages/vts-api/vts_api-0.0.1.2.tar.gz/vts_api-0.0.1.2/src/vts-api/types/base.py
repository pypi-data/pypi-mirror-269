from pydantic import BaseModel


class BaseRequest(BaseModel):
	apiName: str
	apiVersion: str
	requestID: str
	messageType: str
	data: dict


class BaseResponse(BaseModel):
	apiName: str
	apiVersion: str
	timestamp: int
	requestID: str
	messageType: str
	data: dict
