FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /waterfrontanalytics
WORKDIR /waterfrontanalytics
COPY requirements.txt /waterfrontanalytics/
RUN pip install -r requirements.txt
COPY . /waterfrontanalytics/