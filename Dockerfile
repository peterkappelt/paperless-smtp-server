FROM python:3.11-alpine

WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --system
COPY *.py .

CMD ["python3", "-m", "main"]
