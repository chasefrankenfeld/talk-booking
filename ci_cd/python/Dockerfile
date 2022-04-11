FROM python:3.9-slim
RUN mkdir -p /home/github && addgroup github && useradd -d /home/github -g github github && chown github:github /home/github
RUN apt-get update && apt-get install -y curl
USER github
WORKDIR /home/github
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH=/home/github/.poetry/bin:$PATH
RUN poetry config virtualenvs.in-project true
