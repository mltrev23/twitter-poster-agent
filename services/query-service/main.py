# Let create something with FastAPi
from fastapi import FastAPI


app = FastAPI()

@app.get("/query-service")
def query_stream():
    return {"Hello","World"}