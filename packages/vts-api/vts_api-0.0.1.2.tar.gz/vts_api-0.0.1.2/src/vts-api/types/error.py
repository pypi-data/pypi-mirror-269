from pydantic import BaseModel


class APIError(BaseModel):
	errorID: int
	message: str
