FROM python:3

WORKDIR /app/backend
COPY requirements.txt /app/backend
COPY . /app/backend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pymongo==4.2.0
