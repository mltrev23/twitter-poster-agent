# Let create something with FastAPi
from fastapi import FastAPI


app = FastAPI()


@app.get("/air-drop")
def query_stream():
    return {"air_drop", "World"}
