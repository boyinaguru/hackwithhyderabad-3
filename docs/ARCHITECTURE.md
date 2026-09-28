# Architecture

```
                 ┌─────────────────────┐
                 │      React UI       │
                 │ Customer + Chat UI  │
                 │   Memory Timeline   │
                 └──────────┬──────────┘
                            │ HTTP
                            ▼
                 ┌─────────────────────┐
                 │      FastAPI        │
                 │   Support Agent     │
                 └──────┬───────┬──────┘
                        │       │
                 Recall │       │ LLM
                        ▼       ▼
                ┌──────────┐  ┌──────────┐
                │ Hindsight│  │ LLM API  │
                │  Memory  │  │  Groq    │
                └────┬─────┘  └────┬─────┘
                     │              │
                     └──────┬───────┘
                            ▼
                    Personalized Reply

After each meaningful interaction:
FastAPI -> Hindsight Retain

Before each response:
User issue -> Hindsight Recall -> LLM context -> answer
```
