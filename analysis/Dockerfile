FROM python:3.8
WORKDIR /analysis

ARG creds

COPY CCCAssignment2/analysis/ ./
RUN pip install -r requirements.txt

COPY $creds "credentials1.json"

CMD ["python3", "analysis.py"]
