# Open-WebUI Auto Idle
## Why
I do not want a docker container to continously run when noone is using it.

## How
Run `watchdog.sh` every minute to check for active connections on port 9003 (or whereever your Open-WebUI runs)
```bash
crontab -e
```
```
* * * * * /opt/llm/watchdog.sh > /opt/llm/watchdog.log
```

## Result
* `docker compose -f docker-compose.yml up -d` if active connection
* `docker compose -f docker-compose.yml down` if no active connection in the last minute

