FROM python:slim

RUN pip install requests pymongo

RUN mkdir /app

COPY monitor/ /app

WORKDIR /

CMD ["python", "-mapp"]
