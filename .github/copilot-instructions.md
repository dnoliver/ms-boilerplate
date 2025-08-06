# Microservice Boilerplate (ms-boilerplate)

**ALWAYS follow these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

A Python FastAPI microservice boilerplate with comprehensive development tooling, containerization, and CI/CD pipeline.

## Working Effectively

### Bootstrap and Setup
- Install Poetry: `pip install poetry==2.1.3` (takes ~30 seconds)
- Install project dependencies: `poetry install` (takes ~20 seconds, NEVER CANCEL)
- Set timeout: 60+ seconds for initial setup to handle potential network delays

### Build and Test Commands
- Run linting: `poetry run lint` (takes ~4 seconds)
- Run security scan: `poetry run scan` (takes ~1 second)
- Run unit tests: `poetry run unittest` (takes ~1-2 seconds)
- Run formatting check: `poetry run black --check .` (takes ~1 second)
- Run import sorting check: `poetry run isort --check-only .` (takes ~1 second)

### Application Execution
- Start application: `poetry run app`
  - Application runs on http://0.0.0.0:8000
  - API documentation at http://0.0.0.0:8000/docs
  - Takes ~3 seconds to start up
  - NEVER CANCEL: Let the server fully initialize before testing

### Docker Operations
- **NETWORK LIMITATION**: Docker builds may fail due to network restrictions in some environments
- Build development image: `docker build --target dev -t ms-boilerplate-dev .`
- Build builder image: `docker build --target builder -t ms-boilerplate-builder .`
- Build runtime image: `docker build -t ms-boilerplate .`
- Run with compose: `docker compose up`
- **TIMEOUT WARNING**: Docker builds can take 5-10 minutes. Set timeout to 15+ minutes, NEVER CANCEL

### Pre-commit Hooks
- **NETWORK LIMITATION**: Pre-commit hooks (`poetry run pre-commit run --all-files`) may fail due to network restrictions
- Individual tools work: `poetry run black .`, `poetry run isort .`, `poetry run pylint .`

## Validation Scenarios

### Critical End-to-End Testing
**ALWAYS test these scenarios after making changes:**

1. **API Health Check**:
   ```bash
   curl -s http://localhost:8000/
   # Expected: {"message":"Hello, FastAPI!"}
   ```

2. **Division Endpoint - Success**:
   ```bash
   curl -s "http://localhost:8000/divide?a=10&b=2"
   # Expected: {"result":5.0}
   ```

3. **Division Endpoint - Error Handling**:
   ```bash
   curl -s "http://localhost:8000/divide?a=10&b=0"
   # Expected: {"detail":"Division by zero is not allowed"}
   ```

4. **JSON Formatting - Success**:
   ```bash
   curl -s -X POST "http://localhost:8000/format" -H "Content-Type: application/json" -d '{"json_string": "{\"name\":\"John\",\"age\":30}"}'
   # Expected: {"formatted":"{\n  \"name\": \"John\",\n  \"age\": 30\n}"}
   ```

5. **JSON Formatting - Error Handling**:
   ```bash
   curl -s -X POST "http://localhost:8000/format" -H "Content-Type: application/json" -d '{"json_string": "invalid json"}'
   # Expected: {"detail":"Invalid JSON string: ..."}
   ```

6. **Documentation Access**:
   ```bash
   curl -s http://localhost:8000/docs | grep -o '<title>.*</title>'
   # Expected: <title>FastAPI - Swagger UI</title>
   ```

### CI/CD Validation Steps
**ALWAYS run before committing changes:**
1. `poetry run lint` (must pass with 10.00/10 rating)
2. `poetry run scan` (must show "No issues identified")
3. `poetry run unittest` (all 10 tests must pass)
4. `poetry run black --check .` (must show "would be left unchanged")
5. `poetry run isort --check-only .` (must complete without changes)

## Critical Timing Information

### Command Timeouts (NEVER CANCEL)
- `poetry install`: 20 seconds normally, **set timeout to 120+ seconds**
- `poetry run lint`: 4 seconds normally, **set timeout to 60 seconds**
- `poetry run unittest`: 1-2 seconds normally, **set timeout to 30 seconds**
- `poetry run app`: 3 seconds to start, **set timeout to 60 seconds for startup**
- Docker builds: 2-10 minutes normally, **set timeout to 20+ minutes, NEVER CANCEL**
- Pre-commit hooks: 30 seconds+ normally, **set timeout to 300+ seconds**

### Network-Dependent Operations
**These may fail in restricted environments:**
- Docker builds (requires PyPI access for poetry installation)
- Pre-commit hook installation (requires GitHub/PyPI access)
- Poetry installation via curl (use `pip install poetry==2.1.3` instead)

## Key Project Structure

### Essential Files and Directories
```
/home/runner/work/ms-boilerplate/ms-boilerplate/
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI application code
├── test/
│   ├── __init__.py
│   └── test_main.py         # Unit tests (10 test cases)
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI pipeline with linting, testing, security
│       └── agent.yml        # SWE-Agent automation
├── pyproject.toml           # Poetry configuration and dependencies
├── poetry.lock              # Locked dependency versions
├── scripts.py               # Poetry script definitions
├── Dockerfile               # Multi-stage Docker build
├── compose.yml              # Docker Compose configuration
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── .pylintrc                # Pylint configuration
└── README.md                # Basic project documentation
```

### Core Dependencies
- **Runtime**: FastAPI 0.116.1, Python 3.12
- **Development**: Poetry 2.1.3, Black 25.1.0, Pylint 3.3.7, Bandit 1.8.6, isort 6.0.1
- **Testing**: unittest (Python standard library), FastAPI TestClient

## Common Tasks Reference

### Frequently Used Commands Output
```bash
# Repository root listing
ls -la
# Shows: app/, test/, .github/, pyproject.toml, poetry.lock, Dockerfile, compose.yml, scripts.py

# Check Poetry configuration
poetry show --tree
# Shows: dependency tree with FastAPI and dev tools

# List available Poetry scripts
poetry run --help
# Shows: lint, scan, unittest, app commands
```

### FastAPI Application Details
- **Framework**: FastAPI with Uvicorn server
- **Endpoints**: 
  - `GET /` - Health check
  - `GET /divide?a=<float>&b=<float>` - Division with error handling
  - `POST /format` - JSON formatting utility
- **Features**: Automatic OpenAPI documentation, Pydantic validation, error handling
- **Production**: Ready for containerization and deployment

### Development Workflow
1. **Setup**: `pip install poetry==2.1.3 && poetry install`
2. **Code**: Make changes to `app/main.py` or tests in `test/`
3. **Validate**: Run all CI commands (`lint`, `scan`, `unittest`)
4. **Test**: Start app with `poetry run app` and validate endpoints manually
5. **Format**: Use `poetry run black .` and `poetry run isort .` if needed
6. **Commit**: Ensure all validation passes before committing

### Troubleshooting
- **"poetry: command not found"**: Install with `pip install poetry==2.1.3`
- **Network timeouts**: Docker and pre-commit may fail due to network restrictions - use individual tools
- **Import errors**: Ensure `poetry install` completed successfully
- **Port conflicts**: Default port is 8000, check if already in use
- **Test failures**: Run `poetry run unittest` for detailed error output

## Environment Notes
- **Python Version**: 3.12+ required
- **Container Platform**: Docker with multi-stage builds
- **CI/CD**: GitHub Actions with comprehensive testing pipeline
- **Code Quality**: Enforced via pylint, black, isort, bandit, and pre-commit hooks