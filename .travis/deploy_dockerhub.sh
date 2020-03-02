#!/bin/bash
docker login -u "$DOCKER_ACCOUNT" -p $DOCKER_PASSWORD

if [ "$TRAVIS_BRANCH" = "master" ]; then
    TAG="latest"
else
    TAG="$TRAVIS_BRANCH"
fi

docker build -f Dockerfile -t $PROJECT_NAME:$TAG .
docker tag $PROJECT_NAME $DOCKER_REPO
docker push $DOCKER_REPO