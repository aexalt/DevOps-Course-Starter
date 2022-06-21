FROM python:buster as base

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry gunicorn markupsafe==2.0.1
RUN mkdir /todo_app 
COPY /todo_app /todo_app
COPY pyproject.toml /
COPY .env /
COPY gunicorn_config.py /
COPY run.sh /
COPY poetry.lock /
WORKDIR /todo_app

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
WORKDIR /
#RUN chmod +x ./run.sh

FROM base as production
ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "todo_app.app:create_app()"]
EXPOSE 5000

FROM base as development
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host", "0.0.0.0"]