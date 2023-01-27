FROM python:3.10

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade

COPY requirements.txt /app/requirements.txt

RUN pip install -U -r /app/requirements.txt

COPY . .

VOLUME [ "/app/logs" ]

CMD ["python", "main.py"]
