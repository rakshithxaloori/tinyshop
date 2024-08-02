# aws cloudformation create-stack --stack-name ts-dev-vpc --template-body file://vpc.yaml
# aws cloudformation create-stack --stack-name ts-dev-proxy-ecs --template-body file://proxy-ecs.yaml --parameters file://proxy-ecs-parameters.json --capabilities CAPABILITY_IAM
aws cloudformation create-stack --stack-name ts-dev-api-ecs --template-body file://api-ecs.yaml --parameters file://api-ecs-parameters.json --capabilities CAPABILITY_IAM
