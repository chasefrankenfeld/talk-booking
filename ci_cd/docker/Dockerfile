FROM docker:20.10

# Install AWS
RUN apk add --no-cache aws-cli

# Update python and install poetry
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --update --no-cache curl && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && apk --no-cache del curl
ENV PATH=/root/.poetry/bin:$PATH
