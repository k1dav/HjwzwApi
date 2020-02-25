#!/bin/bash
echo "$DOCKER_ACCOUNT" | docker login -u "$DOCKER_ACCOUNT" -p $DOCKER_PASSWORD
docker push $DOCKER_REPO