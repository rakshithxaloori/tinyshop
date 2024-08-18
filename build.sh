# docker build --no-cache -t ts-proxy-api .
export $(grep -v '^#' .env | xargs) && \
docker build \
-t ts-proxy-api . \
--no-cache \
--build-arg TEST_ENDPOINT=$TEST_ENDPOINT \
--build-arg TEST_DASHBOARD_SECRET=$TEST_DASHBOARD_SECRET \
--build-arg LIVE_DASHBOARD_SECRET=$LIVE_DASHBOARD_SECRET
