FROM python:3.7-slim-buster
WORKDIR /app

EXPOSE 7000
COPY . .

CMD ["echo bonjour"]

RUN pip install -r requirements.txt


CMD [ "python3", "manage.py", "runserver"]
