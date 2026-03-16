from http.server import BaseHTTPRequestHandler
import json
from controllers.rest_response import RestResponse, RestStatus

class ControllerRest:
    def __init__(self, handler: BaseHTTPRequestHandler):
        self.handler = handler
        self.rest_response = RestResponse() 

    def before_execution(self):
        pass

    def after_execution(self):
        pass

    def serve(self): 
        mname = 'do_' + self.handler.command
        if not hasattr(self, mname):
            self.rest_response.status = RestStatus( 
                is_ok = False,
                code = RestStatus.METHOD_NOT_ALLOWED.code,
                phrase= f"{RestStatus.METHOD_NOT_ALLOWED.phrase}: Unsupported method ({self.handler.command}) in '{self.__class__.__name__}'"
            )
        else:
            method = getattr(self, mname)
            try:
                self.before_execution()
                method()
                self.after_execution()
            except Exception as ex:
                self.rest_response.status = RestStatus( 
                    is_ok = False,
                    code = RestStatus.INTERNAL_SERVER_ERROR.code,
                    phrase = f"{RestStatus.INTERNAL_SERVER_ERROR.phrase}: {str(ex)}"
                )
        self.send_rest_response()    

    def send_rest_response(self):
        self.handler.send_response(self.rest_response.status.code, self.rest_response.status.phrase)
        self.handler.send_header("Content-Type", "application/json; charset=utf-8")
        self.handler.end_headers()
        self.handler.wfile.write(
            json.dumps(
                self.rest_response, 
                ensure_ascii=False,
                default=lambda x: x.__json__() if hasattr(x, "__json__") else str
            ).encode()
        )