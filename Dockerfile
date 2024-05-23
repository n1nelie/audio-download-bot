FROM python:3.11

WORKDIR /app

COPY main.py /app
COPY requirements.txt /app
COPY /secrets /app/secrets

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
