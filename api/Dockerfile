FROM python:3.11-slim

# USED TO BE RUN mkdir /apicode
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app/

EXPOSE 4000

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

