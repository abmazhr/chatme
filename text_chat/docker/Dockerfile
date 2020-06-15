FROM node:14.4.0-alpine3.12

LABEL name="Abdulrahman" email="abmazhr@gmail.com"

RUN apk add --no-cache g++ make bash # for our builds

ENV APP_PATH /usr/app/
RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

ADD package.json  $APP_PATH
ADD Makefile      $APP_PATH
ADD build.ts      $APP_PATH
ADD tsconfig.json $APP_PATH
ADD .env          $APP_PATH

RUN make prepare-env-locally

COPY src $APP_PATH/src

EXPOSE 3001

ENTRYPOINT ["sh", "-c", "make run-server-native-locally"]