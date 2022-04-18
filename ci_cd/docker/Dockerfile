FROM docker:19.03

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --update --no-cache curl && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && apk --no-cache del curl
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
ENV PATH=/root/.poetry/bin:$PATH
