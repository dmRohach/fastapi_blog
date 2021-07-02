FROM python:3.8-slim

COPY ./src /fastapi_blog/src
COPY ./requirements.txt /fastapi_blog
COPY ./database.sqlite3 /fastapi_blog

WORKDIR /fastapi_blog

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host=0.0.0.0"]