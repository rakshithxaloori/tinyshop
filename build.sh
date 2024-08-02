# docker build --nocache -t ts-api-test .

export $(grep -v '^#' .env | xargs) && \
docker build \
-t ts-api-test . \
--no-cache \
--build-arg DB_URL=$DB_URL \
--build-arg RAZORPAY_KEY_ID=$RAZORPAY_KEY_ID \
--build-arg RAZORPAY_KEY_SECRET=$RAZORPAY_KEY_SECRET
