FROM python:slim

RUN pip install requests pymongo

RUN mkdir /app

COPY classifier/ /app

WORKDIR /

CMD ["python", "-mapp"]
