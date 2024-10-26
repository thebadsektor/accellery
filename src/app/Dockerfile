# pull official base image
FROM python:3.11.2-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# copy requirements from the root directory
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy the entire project
COPY ./src/app .

# entrypoint command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
