FROM docker:20.10

# Install AWS
RUN apt-get update && \
    apt-get install -y \
        unzip \
        curl \
    && apt-get clean \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf \
        awscliv2.zip \
    && apt-get -y purge curl \
    && apt-get -y purge unzip 

# Update python and install poetry
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --update --no-cache curl && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && apk --no-cache del curl
ENV PATH=/root/.poetry/bin:$PATH
