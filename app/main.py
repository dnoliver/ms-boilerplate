"""FastAPI application main module."""

import json
from typing import Optional

import yaml
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

app = FastAPI()


class JsonFormatRequest(BaseModel):
    """Request model for JSON formatting."""

    json_string: str


class YamlFormatRequest(BaseModel):
    """Request model for YAML formatting."""

    yaml_string: str


class FormatRequest(BaseModel):
    """Unified request model for formatting."""

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
    content_type = request.headers.get("content-type", "application/json")
    
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        
        if content_type == "application/yaml":
            # Parse request body as YAML
            try:
                parsed_data = yaml.safe_load(body_str)
            except yaml.YAMLError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid YAML request body: {str(e)}"
                ) from e
            
            # Check for yaml_string field
            if not isinstance(parsed_data, dict) or "yaml_string" not in parsed_data:
                raise HTTPException(
                    status_code=400, 
                    detail="Request body must contain 'yaml_string' field when using application/yaml content type"
                )
            
            yaml_string = parsed_data["yaml_string"]
            
            try:
                # Parse the YAML string content
                parsed_yaml = yaml.safe_load(yaml_string)
                # Format it with proper indentation  
                formatted_yaml = yaml.dump(parsed_yaml, indent=2, default_flow_style=False)
                return {"formatted": formatted_yaml}
            except yaml.YAMLError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid YAML string: {str(e)}"
                ) from e
        
        else:
            # Default to JSON parsing for application/json or other content types
            try:
                parsed_data = json.loads(body_str)
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid JSON request body: {str(e)}"
                ) from e
            
            # Check for json_string field
            if not isinstance(parsed_data, dict) or "json_string" not in parsed_data:
                raise HTTPException(
                    status_code=400, 
                    detail="Request body must contain 'json_string' field when using application/json content type"
                )
            
            json_string = parsed_data["json_string"]
            
            try:
                # Parse the JSON string content
                parsed_json = json.loads(json_string)
                # Format it with proper indentation
                formatted_json = json.dumps(parsed_json, indent=2, ensure_ascii=False)
                return {"formatted": formatted_json}
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid JSON string: {str(e)}"
                ) from e
    
    except UnicodeDecodeError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid request body encoding: {str(e)}"
        ) from e
