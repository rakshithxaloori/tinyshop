# Authenticate Docker to the Amazon ECR registry
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 662294483096.dkr.ecr.us-east-1.amazonaws.com

# Tag local Docker image
docker tag ts-proxy-api:latest 662294483096.dkr.ecr.us-east-1.amazonaws.com/ts-proxy-api:latest

# Push the Docker image to ECR
docker push 662294483096.dkr.ecr.us-east-1.amazonaws.com/ts-proxy-api:latest
