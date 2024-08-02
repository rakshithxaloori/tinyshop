aws ecs execute-command \
    --cluster ts-dev-proxy-cluster \
    --task 4029e2964b0446e58c131d984f6c910d \
    --container api \
    --interactive \
    --command "/bin/sh"
