# HackwithHyderabad 3.0 Submission Draft

## Project
MemoryDesk AI — Support that remembers.

## Problem
Support teams repeatedly ask customers to explain issues that have already been documented. Knowledge is fragmented across tickets and conversations, so agents often repeat generic troubleshooting.

## Solution
MemoryDesk is a support AI agent that creates persistent customer memory from interactions and recalls relevant history during future support conversations. It uses the remembered context to personalize troubleshooting and avoid repeating already-tried steps.

## Why Hindsight matters
Hindsight is not a decorative feature. The product depends on persistent memory:
- Retain: store important interaction facts.
- Recall: retrieve relevant customer history for the current issue.
- Use: provide the retrieved context to the support agent so the next response is more personalized.
- Demonstrate: surface recalled memories in the UI so judges can see the memory layer.

## 60-second demo
1. Open Rahul Sharma.
2. Ask: “My printer keeps disconnecting from Wi-Fi.”
3. Ask/record that the driver reinstall successfully fixed it.
4. Ask later: “It happened again.”
5. Show the memory panel.
6. The agent references the earlier successful fix instead of restarting from generic troubleshooting.
7. Contrast the first generic response with the later memory-aware response.

## Judging alignment
- Innovation: persistent support memory focused on cumulative issue resolution.
- Hindsight: central memory retrieval and visible memory panel.
- Technical: FastAPI + React + Hindsight + LLM.
- UX: single dashboard with customer, conversation and memory context.
- Real-world impact: less repeated questioning and faster support.

## Team note
Replace the sample/demo data with your team's final synthetic dataset and add team member names before submission.
