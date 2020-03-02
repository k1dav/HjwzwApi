#!/bin/bash

heroku login
heroku container:login
heroku container:push $PROJECT_NAME --app $HEROKU_APP_NAME
heroku container:release $PROJECT_NAME --app $HEROKU_APP_NAME