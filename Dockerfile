FROM python:3.11-slim-buster

WORKDIR /flask-server

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=recommendation_service"]