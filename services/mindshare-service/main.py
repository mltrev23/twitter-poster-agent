# Let create something with FastAPi
from fastapi import FastAPI


app = FastAPI()

@app.get("/mindshare-service")
def mindshare_stream():
    return {"Hello","World"}