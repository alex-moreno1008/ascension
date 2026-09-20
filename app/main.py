from fastapi import FastAPI

app = FastAPI(title="Ascension")


@app.get("/")
def read_root():
    return {"message": "Welcome to Ascension"}