from fastapi import FastAPI,Request, HTTPException
from limiter.fixed_window import FixedWindow
from limiter.sliding_window import SlidingWindow
from limiter.token_bucket import TokenBucketLimiter
from fastapi.responses  import JSONResponse
app = FastAPI()

fixedwindow = FixedWindow(10,60)
slidingwindow = SlidingWindow(10,60)
tokenBucket = TokenBucketLimiter(2, 1)  
@app.middleware("http")
async def rate_limiting(request: Request, call_next):
    ok = tokenBucket.is_allowed(request.client.host)
    if not ok:
        return JSONResponse(status_code=429, content={"details": "Rate Limit Exceeded"})
    response = await call_next(request)
    return response




@app.get("/")
def get_root():
    return {"hello":"world"}