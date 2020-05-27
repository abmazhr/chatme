FROM python:3.8.3-alpine3.11

LABEL name="Abdulrahman" email="abmazhr@gmail.com"

RUN apk add --no-cache g++ make bash # for our builds
RUN pip3 install --upgrade pip

ENV APP_PATH /usr/src/
RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

ADD Pipfile $APP_PATH
ADD Makefile $APP_PATH

RUN pip3 install pipenv

COPY src $APP_PATH/src

EXPOSE 3000

ENTRYPOINT ["sh", "-c", "make run-server-native-locally"]