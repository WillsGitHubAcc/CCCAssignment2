FROM python:3.8

WORKDIR /uid_server

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py .

CMD ["python", "user_dispatch_server.py", "-k", "credentials.json"]