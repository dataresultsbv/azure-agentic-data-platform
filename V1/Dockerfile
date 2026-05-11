## We create app-user to prevent running from ROOT for security improvements

FROM python:3.11-slim

ARG APP_VERSION=V1

RUN groupadd -r app-user && useradd -r -g app-user app-user

WORKDIR /app

COPY ${APP_VERSION}/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ${APP_VERSION}/src/simulation ./src/simulation

RUN chown -R app-user:app-user /app

USER app-user

CMD ["python", "simulator/main.py"]