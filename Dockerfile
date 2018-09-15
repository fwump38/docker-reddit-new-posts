FROM python:3-slim

MAINTAINER David Mirch fwump38@gmail.com

# Setup script directory
RUN mkdir /home/fwump38
ADD ./requirements.txt /home/fwump38/requirements.txt

#Update python requeriments
RUN pip install -r /home/fwump38/requirements.txt

#Add python script to docker container and grant execution rights
ADD ./submissions.py /home/fwump38/submissions.py
RUN chmod +x /home/fwump38/submissions.py

# Start the script
CMD python /home/fwump38/submissions.py