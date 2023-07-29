FROM python:3.10

COPY ./scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./setup.py /setup.py
RUN pip install -e .

COPY ./gunicorn_conf.py /gunicorn_conf.py

WORKDIR /theroast/

COPY ./pip-requirements.txt /theroast/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /theroast/requirements.txt

COPY ./theroast/prestart.sh /theroast/prestart.sh
RUN chmod +x /theroast/prestart.sh

COPY ./theroast /theroast/

ENV PYTHONPATH=/theroast