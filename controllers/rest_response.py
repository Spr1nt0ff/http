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

class RestResponse:
    def __init__(self, status: RestStatus|None=None, data:any=None, meta:dict|None=None):
        self.status = status if status != None else RestStatus()
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