FROM python:3.11-slim

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app/

EXPOSE 4000

RUN pip install -r requirements.txt

# CMD ["python", "-m", "flask", "--app", "backend.rest_entry", "run", "--host=0.0.0.0", "--port=4000"]
CMD [ "python", "app.py"]

