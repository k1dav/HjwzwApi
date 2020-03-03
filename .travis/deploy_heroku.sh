#!/bin/bash
heroku auth:whoami

docker login --username _ --password=$HEROKU_API_KEY registry.heroku.com
heroku container:push $PROJECT_NAME --app $HEROKU_APP_NAME
heroku container:release $PROJECT_NAME --app $HEROKU_APP_NAME