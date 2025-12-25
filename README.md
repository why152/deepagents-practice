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
- [Langgraph CLI](https://langchain-ai.github.io/langgraph/cloud/reference/cli/) (for running the backend server)

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
langgraph dev
```

> **Note**: You need to install the Langgraph CLI to run the server.

#### Start Frontend
```bash
cd frontend
npm run dev
```

## Environment Variables

Check `.env.example` in each sub-directory or the root (if applicable) for required environment variables.


## License

This project is licensed under the terms found in the [LICENSE](LICENSE) file.

For third-party software and licenses used in this project, please see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
