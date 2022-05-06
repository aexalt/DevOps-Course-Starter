FROM python:buster

RUN mkdir /todo_app 
COPY /todo_app /todo_app
COPY pyproject.toml /todo_app
COPY .env /todo_app
COPY gunicorn_config.py /todo_app
COPY run.sh /todo_app
COPY poetry.lock /todo_app
WORKDIR /todo_app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry gunicorn markupsafe==2.0.1
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN chmod +x ./run.sh
EXPOSE 8000
ENTRYPOINT ["sh", "run.sh"]