FROM ubuntu:latest

MAINTAINER Javier Fernandez javier.fernandez@fersacom.es

# Install cron
RUN apt-get update
RUN apt-get install -y -q \
        git  cron nano \
        build-essential \
        python \
        python-yaml \
        python-dev \
        python-setuptools \
        python-pip \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* libssl-dev openssl

#install pip
RUN easy_install -U setuptools && \
    pip install -U pip && \
    pip install --upgrade pip 


# Add crontab file in the cron directory
ADD crontab /etc/cron.d/simple-cron


RUN mkdir /home/fersacom
ADD ./scriptpython/requirements.txt /home/fersacom/requirements.txt
#Update python requeriments
RUN pip install -r /home/fersacom/requirements.txt
#Add python script to docker container
ADD ./scriptpython/test.py /home/fersacom/test.py

# Add shell script and grant execution rights
ADD ./scriptpython/scriptpython.sh /home/fersacom/scriptpython.sh
RUN chmod +x /home/fersacom/scriptpython.sh

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
