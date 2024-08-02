# docker build --no-cache -t ts-proxy-api .
export $(grep -v '^#' .env | xargs) && \
docker build \
-t ts-proxy-api . \
--no-cache \
--build-arg TEST_ENDPOINT=$TEST_ENDPOINT \
