import base64

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()


@app.middleware("http")
async def get_credentials(request: Request, call_next):
    auth = request.headers.get("Authorization")
    scheme, data = (auth or " ").split(" ", 1)
    if scheme != "Basic":
        return JSONResponse(
            content={"message": "Only Basic Authentication is allowed"},
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )

    username, _ = base64.b64decode(data).decode().split(":", 1)
    key_type, mode, _ = username.split("_")
    return JSONResponse(
        content={"message": f"Type: {key_type}; Mode: {mode}"},
        status_code=status.HTTP_200_OK,
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


# docker build -t ts-proxy .

# docker run -d --name ts-proxy-container -p 80:80 ts-proxy

# curl http://127.0.0.1/v1/products \
#   -u sk_test_tR3PYbcVNZZ796tH88S4VQ2u:
