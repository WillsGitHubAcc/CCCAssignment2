FROM python:3.8

WORKDIR /db_api_flask

EXPOSE 3001 5984

ARG creds

COPY CCCAssignment2/db_api_flask/requirements.txt .
RUN pip install -r requirements.txt
COPY CCCAssignment2/db_api_flask/db_api_server.py .
COPY $creds "credentials.json"

CMD [ "python3", "db_api_server.py", "-k", "credentials.json" ]
