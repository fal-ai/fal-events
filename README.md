### what is this?

reference implementation of event collection and analysis with duckdb buenavista and fal-serverless

### Get started

1. install required dependencies

```
pip install fal-serverless
```

```
fal-serverless auth login
```

2. expose endpoint

```
@isolated(requirements=["duckdb"], serve=True)
def save_event(event):
    import duckdb
    import json

    con = duckdb.connect("/data/duck.db")
    con.sql("CREATE TABLE IF NOT EXISTS events (j JSON);")
    query = f"INSERT INTO events VALUES('{json.dumps(event)}')"
    con.sql(query)
    return
```

to expose the function save_event function in the events.py file run the following command:

```
fal-serverless function serve ./fal-events/src/events.py save_event --alias save
```

to expose the buenavista server run the following command:

```
fal-serverless function serve ./fal-events/src/events.py query --alias query
```

3. connect to duckdb using presto cli

install the presto cli using the following link, [presto cli](https://prestodb.io/docs/current/installation/cli.html)

first, generate auth keys with fal-serverless

```
fal-serverless key generate
```

finally, connect to your endpoint exposing the buenavista endpoint:

```
presto --server "https://1714827-query.gateway.alpha.fal.ai?fal_key_id=xxx&fal_key_secret=xxx"
```

4. you can use this url to connect your duckdb instance your favorite BI tool
