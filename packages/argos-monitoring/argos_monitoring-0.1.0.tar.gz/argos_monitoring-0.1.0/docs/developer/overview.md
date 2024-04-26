# Technical overview

Argos uses an agent and server architecture. The server is responsible for storing the configuration and the results of the checks. The agent is responsible for running the checks and sending the results to the server.

## Sequence diagram

```{mermaid}
sequenceDiagram
    participant Agent
    participant Server
    loop
        Agent->>Server: Hey, do you have some work for me?
        Server-->>Agent: Here is some work
        Agent->>Agent: Run checks
        Agent->>Server: Here are the results
        Server->>Server: Determine severity
        Server->>Server: Store results
    end
```

## Orchestration

The server acts like a job queue. When an agent asks for work, the server will:
- mark the tasks as "selected by" the agent
- store the current date
  
When it receives the results, it will:
- Remove the "selected by" and "selected at" fields
- Compute the next execution date.
- Send alerts if needed
