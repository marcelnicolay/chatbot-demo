# Building a Chatbot agent with langchain

This is a chatdemo project bootstrapped with FastApi for backend and NextJs for frontend.

## Features
- Act as a product guidance assistant using ChatGPT
- Keep track of its progress, and don’t forget along the lines of what it already knows.
- We want the agent to be specialized in product usage, acquiring the needed knowledge via retrieval augmentation.

## Getting Started

First, go to backend directory:

```bash
cd backend
```

Copy and edit local .env file

```bash
cp .env.example .env
```

Start webserver using docker

```bash
docker compose up --build
``` 

Go to frontend directory

```bash
cd frontend
```

Copy and edit local .env file

```bash
cp .env.example .env.local
```

Start front end
```bash
npm run dev
``` 

Open http://localhost:3000

## The chat instructed like this

## Prompt examples based in the FAQ base example
- Can you draft email responses?
- How pricing is determined?
- What outreach channels are in development?
- How does you handle email communication?
- Where does you get leads from?

## Development decisions
- Python/fastapi as api backend server 
- Langchain integrated with OpenAI/ChatGPT Model
- Nextjs/react as frontend with basic components
- Use mongodb to show persistence approach with stored data
- Use chromadb as vector storage database to show RAG approach to LLM
- Implementing basic rest api to handle chat iteractions
- Use docker to run webserver
- Testing for backend api routes

## With more time I'll possible do
- Upgrade chat to support streaming text and improve user experience
- Use simple-oauth2 with fake users base db to show authentication approach
- Implement some tools in the chat and caching LLM responses to saving costs
- Use github actions/secrets to run tests and continous integrate code in dev/prod
- Implement tests for react component
- Instrument systems with some observability tool, such as newrelic, datadog, or similar to track bugs and performance

## Project structure

```
$PROJECT_ROOT
└── backend        # backend workdir
    ├── src        # fastapi source files
    ├── data       # RAG vector store
    ├── tests      # Backend tests
└── frontend       # frontend workdir
    ├── src        # nextjs source files
    ├── tests      # frontend tests
```