FROM python:buster as base
RUN pip3 install poetry
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
COPY /todo_app /todo_app
COPY pyproject.toml /

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
RUN poetry install
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host", "0.0.0.0"]