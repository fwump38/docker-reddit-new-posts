FROM python:3

MAINTAINER David Mirch fwump38@gmail.com

# Install cron
RUN apt-get update
RUN apt-get install -y -q \
        git cron nano \
        build-essential \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* libssl-dev openssl

#install pip
RUN easy_install -U setuptools && \
    pip install -U pip && \
    pip install --upgrade pip 


# Add crontab file in the cron directory
ADD crontab /etc/cron.d/simple-cron


RUN mkdir /home/fwump38
ADD ./scriptpython/requirements.txt /home/fwump38/requirements.txt
#Update python requeriments
RUN pip install -r /home/fwump38/requirements.txt
#Add python script to docker container and grant execution rights
ADD ./scriptpython/submissions.py /home/fwump38/submissions.py
RUN chmod +x /home/fwump38/submissions.py

# Add shell script and grant execution rights
ADD ./scriptpython/scriptpython.sh /home/fwump38/scriptpython.sh
RUN chmod +x /home/fwump38/scriptpython.sh

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
