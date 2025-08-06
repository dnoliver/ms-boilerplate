"""FastAPI application main module."""

import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class JsonFormatRequest(BaseModel):
    """Request model for JSON formatting."""

    json_string: str


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


@app.post("/format")
def format_json(request: JsonFormatRequest):
    """Format a JSON string in a human-readable way."""
    try:
        # Parse the JSON string
        parsed_json = json.loads(request.json_string)
        # Format it with proper indentation
        formatted_json = json.dumps(parsed_json, indent=2, ensure_ascii=False)
        return {"formatted": formatted_json}
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid JSON string: {str(e)}"
        ) from e
