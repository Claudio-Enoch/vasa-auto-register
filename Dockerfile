# pull python-alpine image
FROM python:3.8-slim

WORKDIR /usr/src/app

# install dependencies
RUN apt-get update && \
    apt-get install cron -y

# install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# set environment vairables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy vasa-cron file to the cron.d directory
COPY vasa-cron /etc/cron.d/vasa-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/vasa-cron

# Apply cron job
RUN crontab /etc/cron.d/vasa-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

COPY . .
RUN chmod +x main.py

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log