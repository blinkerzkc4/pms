# Base Image
FROM python:3.11

# create and set working directory
RUN mkdir /code
RUN apt update && \
apt install -y fonts-lohit-deva-nepali && \
rm -rf /var/cache/apt/archives /var/lib/apt/lists/*. &&\
 apt-get clean
WORKDIR /code


# Install project dependencies
ADD ./requirements.txt /code/
RUN pip install -r requirements.txt --default-timeout=1000 --no-cache-dir

# Add current directory code to working directory
ADD . /code/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8000
ENV DB_HOST=shangrila-postgres
ENV DB_NAME=yojana_db
ENV DB_USER=yojana_db_user
ENV DB_PASSWORD=YojanaDatabasePassword321
ENV DB_PORT=5432
ENV DEBUG=1


EXPOSE $PORT
CMD python manage.py runserver 0.0.0.0:$PORT
