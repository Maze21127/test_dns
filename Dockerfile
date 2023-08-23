FROM python:3.10

RUN mkdir /fsp_service

WORKDIR /fsp_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD sleep 5 && alembic upgrade heads && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
