FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev

COPY *.py requirements.txt ./
COPY core/ ./core/
COPY routers/ ./routers/
COPY tests/ ./tests/

RUN pip3 install -r requirements.txt
# ENTRYPOINT [""]
