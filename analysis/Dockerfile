FROM python:3.8
WORKDIR /analysis

ARG creds

COPY CCCAssignment2/analysis/analysis.py .
COPY CCCAssignment2/analysis/requirements.txt .
RUN pip install -r requirements.txt

COPY $creds "credentials1.json"

CMD ["python3", "analysis.py"]