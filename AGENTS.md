# AGENTS.md - Development Guidelines for CrewAI Orchestration

## Build/Test Commands

### Python (Main Project)
- **Install**: `pip install -r requirements.txt`
- **Run main**: `python main.py`
- **Single test**: `python test_setup.py` or `python real_ai_test.py`
- **Interactive**: `python interactive_fire.py`

### Frontend (Next.js)
- **Install**: `cd web/frontend && npm install`
- **Dev**: `cd web/frontend && npm run dev`
- **Build**: `cd web/frontend && npm run build`
- **Lint**: `cd web/frontend && npm run lint`

### Backend (FastAPI)
- **Install**: `cd web/backend && pip install -r requirements.txt`
- **Dev**: `cd web/backend && python main.py`
- **Prod**: `cd web/backend && uvicorn main:app --host 0.0.0.0 --port 8000`

## Code Style Guidelines

### Python
- **Imports**: Group (stdlib, third-party, local) with blank lines
- **Formatting**: 4 spaces, max 100 char lines, type hints required
- **Naming**: snake_case for vars/funcs, PascalCase for classes
- **Error handling**: try/except blocks, log errors with context
- **Docs**: Docstrings for all functions and classes

### TypeScript/React
- **Imports**: Use `@/` prefix for internal modules
- **Components**: PascalCase names, default exports
- **Types**: TypeScript interfaces for all props/state
- **Formatting**: Prettier with 2 space indentation
- **Naming**: camelCase for vars/funcs, PascalCase for components

### Configuration & Security
- **Environment**: Use `.env` files, never commit secrets
- **API Keys**: Store in env vars, use `os.getenv()` in Python
- **Validation**: Use Pydantic validators, sanitize user inputs
- **YAML**: 2 spaces indentation, quote strings when needed