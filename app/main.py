"""FastAPI application main module."""
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    """Return a simple greeting message."""
    return {"message": "Hello, FastAPI!"}


@app.get("/divide")
def divide(a: float, b: float):
    """Divide two numbers and return the result."""
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    return {"result": a / b}
