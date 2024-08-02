import os
import base64
import requests
from urllib.parse import urlencode


from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

app = FastAPI()

TEST_ENDPOINT = os.environ["TEST_ENDPOINT"]


@app.middleware("http")
async def get_credentials(request: Request, call_next):
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
        # Construct the new URL with the original path
        new_url = f"{TEST_ENDPOINT.rstrip('/')}{request.url.path}"

        # Extract headers and remove 'host' as it's set by requests automatically
        headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}

        # Properly encode query parameters
        full_url = f"{new_url}?{request.url.query}"

        # Make the request to the TEST_ENDPOINT
        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            data=await request.body(),
            timeout=10,
        )

        # Return the response from the TEST_ENDPOINT
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )

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
