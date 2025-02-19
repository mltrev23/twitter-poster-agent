from fastapi import FastAPI

app = FastAPI()

@app.get("/lulu-service")
def lulu_stream():
    return {"Hello","World"}