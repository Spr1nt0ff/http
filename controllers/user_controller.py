from http.server import BaseHTTPRequestHandler
from controllers.controller_rest import ControllerRest
import math 

class UserController(ControllerRest):
    def __init__(self, handler: BaseHTTPRequestHandler):
        super().__init__(handler)

    def do_GET(self):
        all_users = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Carol", "email": "carol@example.com"},
            {"id": 4, "name": "Dave", "email": "dave@example.com"},
            {"id": 5, "name": "Eve", "email": "eve@example.com"},
            {"id": 6, "name": "Frank", "email": "frank@example.com"},
            {"id": 7, "name": "Grace", "email": "grace@example.com"},
            {"id": 8, "name": "Heidi", "email": "heidi@example.com"},
            {"id": 9, "name": "Ivan", "email": "ivan@example.com"},
            {"id": 10, "name": "Judy", "email": "judy@example.com"},
            {"id": 11, "name": "Mallory", "email": "mallory@example.com"},
            {"id": 12, "name": "Trent", "email": "trent@example.com"}
        ]

        params = self.handler.query_params
        
        try:
            page = int(params.get("page", 1))
        except ValueError:
            page = 1
            
        try:
            per_page = int(params.get("per_page", 2))
        except ValueError:
            per_page = 2

        total_items = len(all_users)
        total_pages = math.ceil(total_items / per_page)
        
        if page < 1: page = 1
        if page > total_pages and total_pages > 0: page = total_pages

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_data = all_users[start_idx:end_idx]

        path_parts = self.handler.path.split('?', 1)
        raw_query_string = path_parts[1] if len(path_parts) > 1 else ""

        self.rest_response.data = {
            "users": paginated_data,              
            "query_string": raw_query_string,    
            "query_params": params,               
            "api": self.handler.api               
        }

        self.rest_response.meta = {
            "count": len(paginated_data),
            "total_items": total_items,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "has_prev": page > 1,
                "has_next": page < total_pages
            }
        }