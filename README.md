# ONO Media OK news forwarder

Forwards news from ONO Media API to OK groups.



## How to run
* Build image
```bash
docker build -t ono-news-forwarder
```

* Run
```bash
docker run --name news-forwarder --env-file env ono-news-forwarder
```

## Environment variables
```
POST_TIME - Post interval
APPLICATION_ID
ACCESS_TOKEN
SESSION_SECRET_KEY
APPLICATION_KEY
GROUP_ID
```
