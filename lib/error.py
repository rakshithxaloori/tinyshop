from fastapi import HTTPException


class TinyshopException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_type: str,
        code: str = None,
        decline_code: str = None,
        message: str = None,
        param: str = None,
        detail: str = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.type = error_type
        self.code = code
        self.decline_code = decline_code
        self.message = message
        self.param = param
