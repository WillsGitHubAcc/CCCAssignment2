FROM python:3.8

WORKDIR /twitter_harvester

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py .

CMD ["python", "twitter_harvester.py", "-m", "stream", "-c", "config.json", "-k", "credentials.json"]