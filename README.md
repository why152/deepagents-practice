# My Unified Project

This repository contains both the frontend and backend components of the project.

## Project Structure

- **`/frontend`**: [Next.js](https://nextjs.org/) based web application.
- **`/backend`**: [Langgraph](https://langchain-ai.github.io/langgraph/) based agentic AI backend.

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (3.11+)
- [Poetry](https://python-poetry.org/) (for backend dependency management)

### Installation

#### Frontend
```bash
cd frontend
npm install
```

#### Backend
```bash
cd backend
poetry install
```

### Running the Project

#### Start Backend
```bash
cd backend
poetry run python my_agent/agent.py # or the appropriate entry point
```

#### Start Frontend
```bash
cd frontend
npm run dev
```

## Environment Variables

Check `.env.example` in each sub-directory or the root (if applicable) for required environment variables.

## License

This project is licensed under the terms found in the [LICENSE](LICENSE) file.
