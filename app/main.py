"""FastAPI application main module."""

import json
from typing import Optional

import yaml
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

app = FastAPI()


class FormatRequest(BaseModel):
    """Request model for formatting JSON or YAML."""

    json_string: Optional[str] = None
    yaml_string: Optional[str] = None


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
async def format_content(request: Request):
    """Format a JSON or YAML string in a human-readable way."""
    # Get content type
    content_type = request.headers.get("content-type", "application/json")
    
    # Parse the request body
    try:
        if content_type.startswith("application/yaml"):
            # Handle YAML content type
            body = await request.body()
            # Parse as JSON first to get the structure
            try:
                data = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid request body: {str(e)}"
                ) from e
            
            if "yaml_string" in data:
                yaml_content = data["yaml_string"]
                try:
                    # Parse and format YAML
                    parsed_yaml = yaml.safe_load(yaml_content)
                    formatted_yaml = yaml.dump(parsed_yaml, default_flow_style=False, indent=2)
                    return {"formatted": formatted_yaml.strip()}
                except yaml.YAMLError as e:
                    raise HTTPException(
                        status_code=400, detail=f"Invalid YAML string: {str(e)}"
                    ) from e
            else:
                raise HTTPException(
                    status_code=400, detail="yaml_string field is required for YAML content type"
                )
        else:
            # Handle JSON content type (default behavior)
            body = await request.body()
            try:
                data = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid request body: {str(e)}"
                ) from e
            
            # Check for json_string or yaml_string
            if "json_string" in data:
                json_content = data["json_string"]
                try:
                    # Parse and format JSON
                    parsed_json = json.loads(json_content)
                    formatted_json = json.dumps(parsed_json, indent=2, ensure_ascii=False)
                    return {"formatted": formatted_json}
                except json.JSONDecodeError as e:
                    raise HTTPException(
                        status_code=400, detail=f"Invalid JSON string: {str(e)}"
                    ) from e
            elif "yaml_string" in data:
                yaml_content = data["yaml_string"]
                try:
                    # Parse and format YAML
                    parsed_yaml = yaml.safe_load(yaml_content)
                    formatted_yaml = yaml.dump(parsed_yaml, default_flow_style=False, indent=2)
                    return {"formatted": formatted_yaml.strip()}
                except yaml.YAMLError as e:
                    raise HTTPException(
                        status_code=400, detail=f"Invalid YAML string: {str(e)}"
                    ) from e
            else:
                raise HTTPException(
                    status_code=400, detail="Either json_string or yaml_string field is required"
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        ) from e
