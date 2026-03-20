from http.server import BaseHTTPRequestHandler
from controllers.controller_rest import ControllerRest
from controllers.rest_response import RestPagination
import math 


class ProductController(ControllerRest):
    def __init__(self, handler: BaseHTTPRequestHandler):
        super().__init__(handler)

    def do_GET(self):
        # Зразкові товари
        all_products = [
            {"id": 1, "name": "Ноутбук", "price": 15000, "description": "Портативний комп'ютер"},
            {"id": 2, "name": "Монітор", "price": 3500, "description": "Екран 27 дюймів"},
            {"id": 3, "name": "Клавіатура", "price": 800, "description": "Механічна клавіатура"},
            {"id": 4, "name": "Миш", "price": 400, "description": "Бездротова миш"},
            {"id": 5, "name": "Навушники", "price": 2000, "description": "Бездротові навушники"},
            {"id": 6, "name": "Веб-камера", "price": 600, "description": "Full HD камера"},
            {"id": 7, "name": "SSD диск", "price": 4000, "description": "1TB SSD NVMe"},
            {"id": 8, "name": "Процесор", "price": 8000, "description": "Intel Core i7"},
            {"id": 9, "name": "Відеокарта", "price": 12000, "description": "RTX 4070"},
            {"id": 10, "name": "Оперативна пам'ять", "price": 2500, "description": "DDR5 32GB"},
            {"id": 11, "name": "Блок живлення", "price": 3000, "description": "850W золотий"},
            {"id": 12, "name": "Системний блок", "price": 20000, "description": "Готовий персональний комп'ютер"},
            {"id": 13, "name": "Динаміки", "price": 1200, "description": "2.0 стереодинаміки"},
            {"id": 14, "name": "UPS", "price": 5000, "description": "Безперебійний блок живлення"},
            {"id": 15, "name": "Маршрутизатор", "price": 2000, "description": "Wi-Fi 6 маршрутизатор"},
        ]

        params = self.handler.query_params
        
        try:
            page = int(params.get("page", 1))
        except (ValueError, TypeError):
            page = 1
            
        try:
            per_page = int(params.get("per_page", 3))
        except (ValueError, TypeError):
            per_page = 3

        total_items = len(all_products)
        
        if page < 1: 
            page = 1
        if page > 1 and page > math.ceil(total_items / per_page) and total_items > 0:
            page = math.ceil(total_items / per_page)

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_data = all_products[start_idx:end_idx]

        base_url = f"/product"
        
        pagination = RestPagination(
            page=page,
            per_page=per_page,
            total_items=total_items,
            base_url=base_url
        )

        path_parts = self.handler.path.split('?', 1)
        raw_query_string = path_parts[1] if len(path_parts) > 1 else ""

        self.rest_response.data = {
            "products": paginated_data,              
            "query_string": raw_query_string,    
            "query_params": params,               
            "api": self.handler.api               
        }

        self.rest_response.meta = {
            "count": len(paginated_data),
            "pagination": pagination
        }
