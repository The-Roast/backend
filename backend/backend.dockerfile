FROM python:3.10

WORKDIR /backend

COPY ./pip-requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ./theroast /backend/theroast

CMD ["uvicorn", "backend.theroast.app.main:app", "--host", "0.0.0.0", "--port", "80"]