from fastapi import FastAPI,Request,Response
from starlette.middleware.base import BaseHTTPMiddleware
import random 
import string 
import time 
from collections  import defaultdict
from typing import Dict


class AdvancedMiddleware(BaseHTTPMiddleware):
    def __init__(self,app):
        super().__init__(app)
        self.rate_limit_records: Dict[str,float]= defaultdict(float)
        
    async def log_message(self,message:str):
        print(message)
          
    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        if current_time - self.rate_limit_records[client_ip]<1:
            return Response(content="Rate limit excedded",status_code=429)
        
        self.rate_limit_records[client_ip] = current_time
        path = request.url.path
        await self.log_message(f"Request to {path}")
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() -start_time
        
        
        custom_headers = {"X-Process-Time":str(process_time)}
        for header,value in custom_headers:
            response.headers.append(header,value)
        await self.log_message(f"Response for {path} took {process_time}  seconds")

@app.middleware("http")
async def request_id_logging(request:Request,call_next):
    response  = await call_next(request)
    random_letters = "".join(random.choice(string.ascii_letters) for _ in range(10) )
    print(f'Log {random_letters}')
    response.headers['X-Request-ID'] = random_letters
    return response