FROM python:3.10-alpine3.15

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python" ,"./code/carly_server/carly_server.py"]