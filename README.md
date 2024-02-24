## Run it
**docker-compose up**

Use rabbitmq as broker, and run 2 types of workers. One worker is for general periodic tasks, and another one worker only runs
the specified queue due to some required scenarios. Among those, general tasks, you may want some of them to be rate limited.