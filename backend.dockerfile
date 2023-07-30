FROM python:3.10

COPY ./scripts/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./setup.py /setup.py
RUN pip install -e .

COPY ./gunicorn_conf.py /gunicorn_conf.py

WORKDIR /theroast/

RUN curl -sSL https://install.python-poetry.org| POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /theroast/

RUN poetry config installer.max-workers 10

ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./theroast/prestart.sh /theroast/prestart.sh
RUN chmod +x /theroast/prestart.sh

COPY ./theroast /theroast/

ENV PYTHONPATH=/theroast

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8888", "--reload"]
