FROM tiangolo/uvicorn-gunicorn:python3.10

WORKDIR /app

COPY ./pip-requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./theroast /app
ENV PYTHONPATH=/app