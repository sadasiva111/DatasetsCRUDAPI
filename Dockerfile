FROM python:alpine3.19
RUN apk update && apk add postgresql-client
WORKDIR /app
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY app src
EXPOSE 5000
ENTRYPOINT ["python", "./src/run.py"]