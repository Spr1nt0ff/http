class RestStatus:
    def __init__(self, is_ok:bool =True, code:int = 200, phrase:str = "OK"):
        self.is_ok = is_ok
        self.code = code
        self.phrase = phrase
    
    def __json__(self):
        return {
            "isOk": self.is_ok,
            "code": self.code,
            "phrase": self.phrase,
        }

RestStatus.OK = RestStatus(True, 200, "OK")
RestStatus.CREATED = RestStatus(True, 201, "Created")
RestStatus.BAD_REQUEST = RestStatus(False, 400, "Bad Request")
RestStatus.UNAUTHORIZED = RestStatus(False, 401, "Unauthorized")
RestStatus.FORBIDDEN = RestStatus(False, 403, "Forbidden")
RestStatus.NOT_FOUND = RestStatus(False, 404, "Not Found")
RestStatus.METHOD_NOT_ALLOWED = RestStatus(False, 405, "Method Not Allowed")
RestStatus.URI_TOO_LONG = RestStatus(False, 414, "URI Too Long")
RestStatus.UNSUPPORTED_MEDIA_TYPE = RestStatus(False, 415, "Unsupported Media Type")
RestStatus.INTERNAL_SERVER_ERROR = RestStatus(False, 500, "Internal Server Error")
RestStatus.NOT_IMPLEMENTED = RestStatus(False, 501, "Not Implemented")

class RestResponse:
    def __init__(self, status: RestStatus|None=None, data:any=None, meta:dict|None=None):
        self.status = status if status is not None else RestStatus.OK
        self.data = data
        self.meta = meta 

    def __json__(self):
        response_dict = {
            "status": self.status,
            "data": self.data
        }
        if self.meta is not None:
            response_dict["meta"] = self.meta
            
        return response_dict