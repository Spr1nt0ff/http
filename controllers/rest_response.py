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


class RestPagination:
    """
    Класс для управління метаданими пагінації, включаючи інформацію про наявність
    посилань на попередню та наступну сторінки.
    """
    def __init__(self, page: int, per_page: int, total_items: int, base_url: str = ""):
        self.page = page
        self.per_page = per_page
        self.total_items = total_items
        self.total_pages = (total_items + per_page - 1) // per_page if total_items > 0 else 1
        self.base_url = base_url
        
        # Обчислюємо наявність посилань
        self.has_prev = page > 1
        self.has_next = page < self.total_pages
        
        # Формуємо посилання на попередню та наступну сторінки
        self.prev_url = self._build_url(page - 1) if self.has_prev else None
        self.next_url = self._build_url(page + 1) if self.has_next else None
    
    def _build_url(self, page_num: int) -> str:
        """Будує URL для вказаної сторінки"""
        if not self.base_url:
            return None
        separator = "&" if "?" in self.base_url else "?"
        return f"{self.base_url}{separator}page={page_num}&per_page={self.per_page}"
    
    def __json__(self):
        return {
            "page": self.page,
            "per_page": self.per_page,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "has_prev": self.has_prev,
            "has_next": self.has_next,
            "prev_url": self.prev_url,
            "next_url": self.next_url
        }

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