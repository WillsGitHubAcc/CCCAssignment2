FROM python:3.8

WORKDIR /uid_server

EXPOSE 8001 5984

ARG config
ARG creds

COPY CCCAssignment2/uid_server/requirements.txt .
RUN pip install -r requirements.txt
COPY CCCAssignment2/uid_server/user_dispatch_server.py .
COPY $config "config.json"
COPY $creds "credentials.json"

CMD [ "python3", "user_dispatch_server.py", "-c", "config.json", "-k", "credentials.json"}}]
