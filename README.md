# Building a Chatbot agent with langchain

**The agent instructed like this**
```
1. Act as a product guidance assistant
2. Keep track of its progress, and don’t forget along the lines of what it already knows.
```

**The agent was supposed to overcome these challenges.**
```
1. We want the agent to be specialized in product usage, acquiring the needed knowledge via retrieval augmentation.
2. We want the agent to remember the history of conversation.
```

## Prompt examples
- Is there a way to upload a prospect's base?
- Can you explain how it works?
- How can I create outbound campaing?

## Development decisions
- Use python/fastapi as api backend server and nextjs/react as frontend with basic components (i'm better with backend systems) 
- Use simple-oauth2 with fake users base db to show authentication approach
- Use mongodb to show persistence approach with stored data
- Use local vector storage database to show RAG approach to LLM
- Implementing basic rest api to handle chat iteractions
- Use docker/docker-compose to local development

## With more time I possible do
- Upgrade chat to support streaming text and improve user experience
- Implement some tools in the chat and caching LLM responses to saving costs
- Use github actions/secrets to run tests and continous integrate code in dev/prod
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