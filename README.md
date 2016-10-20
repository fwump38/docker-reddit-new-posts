PARA PODER USAR 
You need to get next folder skell
scriptpyhton/
├── requirements.txt     (requeriments for python)
├── scriptpython.sh      (commando to cron execute)
└── test.py              (comand python that execute scriptpython.sh)

Modify to set date time to execute
* * * * *  /home/fersacom/scriptpython.sh
 ┬ ┬ ┬ ┬ ┬
 │ │ │ │ │
 │ │ │ │ │
 │ │ │ │ └───── day of week (0 - 7) (0 to 6 are Sunday to Saturday, 7 is Sunday again)
 │ │ │ └────────── month (1 - 12)
 │ │ └─────────────── day of month (1 - 31)
 │ └──────────────────── hour (0 - 23)
 └───────────────────────── min (0 - 59)



1º GET PULL FROM IMAGE
docker pull jopo79/dockercronpython

2º RUN WITH VARIABLES 
docker run -t -i -d  jopo79/dockercronpython:latest

EXAMPLE PASSING ENV VARIABLES TO CONTAINER

docker run -t -i -d  -e "PASSWORD=password" -e "EMAIL=email" jopo79/dockercronpython:latest

