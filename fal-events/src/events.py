from fal_serverless import isolated


@isolated(requirements=["duckdb"], serve=True)
def save_event(event):
    """
    This helps you query the duck db instance. Submit events as json here.
    """
    import duckdb
    import json

    con = duckdb.connect("/data/duck.db")
    con.sql("CREATE TABLE IF NOT EXISTS events (j JSON);")
    query = f"INSERT INTO events VALUES('{json.dumps(event)}')"
    con.sql(query)
    return


@isolated(requirements=["duckdb", "buenavista[duckdb]", "uvicorn"], exposed_port=8080)
def query():
    """
    Queries the duck db instance through buena vista. Submit SQL statements here.
    """
    import uvicorn
    import duckdb
    from fastapi import FastAPI
    from buenavista.http import main
    from buenavista.backends.duckdb import DuckDBConnection

    from buenavista import bv_dialects, rewrite

    rewriter = rewrite.Rewriter(bv_dialects.BVTrino(), bv_dialects.BVDuckDB())

    db = duckdb.connect("/data/duck.db")
    app = FastAPI()

    main.quacko(app, DuckDBConnection(db), rewriter)
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
