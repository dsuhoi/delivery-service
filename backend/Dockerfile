FROM python:3.10-slim

WORKDIR /backend_app

RUN apt-get update && apt-get install -y libpq-dev netcat

COPY *.py locations.csv pytest.ini requirements.txt ./
COPY core/ ./core/
COPY routers/ ./routers/
COPY tasks/ ./tasks/
COPY tests/ ./tests/

RUN pip3 install -r requirements.txt

COPY entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/backend_app/entrypoint.sh"]
