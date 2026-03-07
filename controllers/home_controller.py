import os

class HomeController:
    def __init__(self, handler):
        self.handler = handler

    def serve(self):
        mname = 'do_' + self.handler.command
        
        if not hasattr(self, mname):
            self.handler.send_error(405, f"Method {self.handler.command} not allowed")
            return
            
        method = getattr(self, mname)
        method()

    def do_GET(self):
        file_path = "index.html" 
        
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                
            self.handler.send_response(200)
            self.handler.send_header("Content-Type", "text/html; charset=utf-8")
            self.handler.end_headers()
            self.handler.wfile.write(content)
            
        except FileNotFoundError:
            self.handler.send_error(404, "File index.html not found")

    def do_LINK(self):
        self.handler.send_response(200)
        self.handler.send_header("Content-Type", "text/plain; charset=utf-8")
        self.handler.end_headers()
        self.handler.wfile.write("LINK method response received!".encode("utf-8"))