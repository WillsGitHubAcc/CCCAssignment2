FROM python:3.8

WORKDIR /twitter_harvester

EXPOSE 8001 5984

ARG config
ARG creds
ARG mode

COPY CCCAssignment2/twitter_harvester/requirements.txt .
RUN pip install -r requirements.txt
COPY CCCAssignment2/twitter_harvester/twitter_harvester.py .
COPY CCCAssignment2/twitter_harvester/tweet_sanitisers.py .
COPY CCCAssignment2/twitter_harvester/tweet_locations.json .

COPY $config "config.json"
COPY $creds "credentials.json"

# CMD [ "python3", "twitter_harvester.py", "-c", "config.json", "-k", "credentials.json", "-m", {${mode}}}}]
