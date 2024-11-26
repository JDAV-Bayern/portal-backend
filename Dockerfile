FROM python:3.12-bookworm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install deb packages
RUN apt-get update \
    && apt-get install --assume-yes --no-install-recommends \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

ENTRYPOINT [ "./docker-entrypoint.sh" ]
