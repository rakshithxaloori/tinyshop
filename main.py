import os
import base64
import httpx


from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

TEST_ENDPOINT = os.environ["TEST_ENDPOINT"]
TEST_DASHBOARD_SECRET = os.environ["TEST_DASHBOARD_SECRET"]
LIVE_DASHBOARD_SECRET = os.environ["LIVE_DASHBOARD_SECRET"]


DASHBOARD_ERROR_RESPONSE = JSONResponse(
    content={},
    status_code=status.HTTP_404_NOT_FOUND,
)


@app.middleware("http")
async def get_credentials(request: Request, _):
    mode = None
    if request.url.path.startswith("/v1/shops"):
        dashboard_secret = request.headers.get("X-Tinyshop-Dashboard-Secret")
        if dashboard_secret not in [TEST_DASHBOARD_SECRET, LIVE_DASHBOARD_SECRET]:
            return DASHBOARD_ERROR_RESPONSE
        mode, _ = dashboard_secret.split("_")

    else:
        auth = request.headers.get("Authorization")
        scheme, data = (auth or " ").split(" ", 1)
        if scheme != "Basic":
            return JSONResponse(
                content={"message": "Only Basic Authentication is allowed"},
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        try:
            username, _ = base64.b64decode(data).decode().split(":", 1)
            key_type, mode, _ = username.split("_")
        except (ValueError, base64.binascii.Error):
            return JSONResponse(
                content={"message": "Invalid authorization format"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    if mode == "test":
        async with httpx.AsyncClient() as client:
            # Construct the new URL with the original path
            new_url = f"{TEST_ENDPOINT.rstrip('/')}{request.url.path}"
            # Properly encode query parameters
            if request.url.query:
                new_url = f"{new_url}?{request.url.query}"

            response = await client.request(
                method=request.method,
                url=new_url,
                headers=request.headers.raw,
                content=await request.body(),
                timeout=10,
            )
            # Return the response from the TEST_ENDPOINT
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
                headers=dict(response.headers),
            )

    # TODO live

    return JSONResponse(
        content={"message": f"Type: {key_type}; Mode: {mode}"},
        status_code=status.HTTP_200_OK,
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


# docker build -t ts-proxy .

# docker run -d --name ts-proxy-container -p 80:80 ts-proxy

# curl http://127.0.0.1:8081/v1/products \
#   -u sk_test_aunh1MXIU0sUX2nzIcbtMqRR:

# curl http://ts-dev-lb-399352269.us-east-1.elb.amazonaws.com   \
#   -u sk_test_tR3PYbcVNZZ796tH88S4VQ2u:

# curl http://internal-ts-dev-api-lb-1872903523.us-east-1.elb.amazonaws.com/v1/products   \
#   -u sk_test_tR3PYbcVNZZ796tH88S4VQ2u:

# curl https://api.tinyshop.me/v1/products \
#     -u sk_test_hUSong4VleAs44H4fwnYAsIa:
