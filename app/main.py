from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/divide")
def divide(a: float, b: float):
    return {"result": a / b}
