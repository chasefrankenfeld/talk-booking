FROM docker:19.03

RUN apk update && apk add --no-cache curl zip &&  \
    curl -s https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip && \
    unzip awscliv2.zip && ./aws/install

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --update --no-cache curl && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && apk --no-cache del curl
ENV PATH=/root/.poetry/bin:$PATH
