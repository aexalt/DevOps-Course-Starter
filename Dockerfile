FROM python:buster

RUN mkdir /todo_app 
COPY /todo_app /todo_app
COPY pyproject.toml /
COPY .env /
COPY gunicorn_config.py /
COPY run.sh /
COPY poetry.lock /
WORKDIR /todo_app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry gunicorn markupsafe==2.0.1
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
WORKDIR /
RUN chmod +x ./run.sh


ENTRYPOINT ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "todo_app.app:create_app()"]
EXPOSE 5000