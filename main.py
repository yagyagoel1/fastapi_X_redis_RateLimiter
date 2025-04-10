from fastapi import FastAPI,Request, HTTPException
from limiter.fixed_window import FixedWindow
from fastapi.responses  import JSONResponse
app = FastAPI()

fixedwindow = FixedWindow(10,60)


@app.middleware("http")
async def rate_limiting(request:Request,call_back):
    ok = fixedwindow.is_allowed(request.client.host)
    if not ok:
        return  JSONResponse(status_code=429,content={"details":"Rate Limit Exceded"})
    print(ok)
    response =  await call_back(request)
    return response



@app.get("/")
def get_root():
    return {"hello":"world"}