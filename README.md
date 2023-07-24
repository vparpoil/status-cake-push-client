# status-cake-push-client

Python App to push regular updates to status cake

## Type of tests available

### Ping test

Simple ping test

```json
{
    "type": "ping",
    "ip": "8.8.8.8",
    "statusCakeUrl": "https://push.statuscake.com/?PK=PK&TestID=TestID&time=0"
},
```

### Mongo connexion test

Simple mongo connexion test

```json
{
    "type": "mongo",
    "user": "user",
    "password": "password",
    "database": "database",
    "ip": "",
    "statusCakeUrl": "https://push.statuscake.com/?PK=PK&TestID=TestID&time=0"
}
```

### Postgresql connection test

Simple postgresql connection test

```json
{
    "type": "postgresql",
    "user": "user",
    "password": "password",
    "database": "database",
    "ip": "localhost",
    "port": "5432",
    "sslmode": "require",
    "statusCakeUrl": "https://push.statuscake.com/?PK=PK&TestID=TestID&time=0"
}
```

### Curl test with string match

Simple curl test. The result of the curl command is tested with a simple string match

```json
{
    "type": "curl",
    "url": "",
    "textToMatch": "",
    "statusCakeUrl": "https://push.statuscake.com/?PK=PK&TestID=TestID&time=0"
}
```

### Test if a port is open

Simple test to check that a port is opened. Could be use to ensure a service is running as expected.

```json
{
    "type": "port",
    "port": 3131,
    "url": "192.168.1.12",
    "statusCakeUrl": "https://push.statuscake.com/?PK=PK&TestID=TestID&time=0"
}
```

### Requirements

Python is required. There is also a dependency to the pymongo package to test mongo database being up

```
pip install pymongo psycopg2-binary
```

### Installation

create the json to define tests and update it with the tests you need to run and the status cake push URLs

```bash
cp testsSample.json tests.json
vi tests.json
```

add this line to crontab to launch the script every minute (use `which pyhton` to check the location of your python
installation)

```
* * * * * /usr/bin/python /path_to/testRunner.py
```

