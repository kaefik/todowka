---
name: design-to-plan
description: >
  Decompose any application or API design document into a granular, LLM-friendly
  step-by-step implementation plan. Use this skill whenever the user provides a
  design document (API design, app architecture, system spec, PRD, technical spec,
  ERD, or any planning document) and asks to break it into tasks, subtasks, a
  roadmap, implementation steps, sprint plan, or execution checklist. Also trigger
  when user says "разбить на задачи", "составить план реализации", "пошаговый план",
  "декомпозировать документ", "break into tasks", "create implementation plan",
  or "how do I implement this design". The output is a structured plan where every
  step is atomic enough for a single LLM prompt or a single developer task (1–4 hours max).
---

# Design → Implementation Plan

This skill transforms a design document into an **atomic, ordered, LLM-processable** task plan.

---

## Core Principle: Atomic Steps

Every output step must be:
- **Self-contained**: completable without reading other steps
- **Verifiable**: has a clear done condition
- **Sized right**: 1–4 hours of dev work, or 1 focused LLM prompt
- **Dependency-aware**: ordered so each step builds on the previous

---

## Step 1 — Parse the Document

Read the provided document carefully. Extract:

1. **Domain** — what system is being built (API, mobile app, web app, microservice, etc.)
2. **Entities** — data models, resources, objects mentioned
3. **Operations** — CRUD, business logic, flows, integrations
4. **Non-functional requirements** — auth, validation, error handling, performance, security
5. **Dependencies** — external services, libraries, infrastructure
6. **Ambiguities** — anything unclear that needs a decision before coding

If the document is missing critical info (auth strategy, DB choice, deployment target), flag these **before** generating the plan. Ask the user to clarify or make a reasonable assumption and state it explicitly.

---

## Step 2 — Build the Layer Map

Group everything into implementation layers in this order:

```
Layer 0: Foundation        (project setup, config, CI/CD skeleton)
Layer 1: Data Layer        (DB schema, models, migrations, seeders)
Layer 2: Core Business     (services, domain logic, calculations)
Layer 3: API / Interface   (routes, controllers, request/response DTOs)
Layer 4: Auth & Security   (authentication, authorization, middleware)
Layer 5: Integration       (external APIs, queues, webhooks, emails)
Layer 6: Validation & Errors (input validation, error codes, logging)
Layer 7: Tests             (unit, integration, e2e per feature)
Layer 8: Docs & Deployment (API docs, README, deploy scripts)
```

Not all layers are always needed — skip irrelevant ones and say why.

---

## Step 3 — Generate Atomic Tasks

For each layer, produce tasks following this format:

```
### [LAYER_CODE]-[NUMBER] — [Task Title]

**Goal:** One sentence — what this step produces.
**Input:** What you need before starting (files, data, completed steps).
**Output:** Exact artifact produced (file name, endpoint, schema, etc.).
**Done when:** Concrete, testable condition.
**LLM Prompt Hint:** (optional) How to ask an LLM to do this step efficiently.
**Est. effort:** XS / S / M / L  (XS=30min, S=1h, M=2h, L=4h)
```

**Splitting rules:**
- If a task touches more than 1 entity → split per entity
- If a task has more than 3 sub-operations → split into sub-tasks
- If a task requires a decision before implementation → make the decision a separate task (type: `DECISION`)
- If a task is purely documentation → mark as `DOCS`

---

## Step 4 — Output Format

Always output the plan as:

### 1. Summary Table

| # | Layer | Task | Effort | Depends on |
|---|-------|------|--------|------------|
| 1 | Foundation | Init project & env config | S | — |
| 2 | Data Layer | Create User schema & migration | S | 1 |
| … | … | … | … | … |

### 2. Detailed Task Cards

Full cards for every task using the format from Step 3.

### 3. LLM Execution Guide (if requested)

How to feed these tasks to an LLM in sequence:
- System prompt to set context once
- Order of prompts
- What to pass as context between steps (output of step N → input of step N+1)

---

## Step 5 — Quality Checks

Before finalizing, verify:

- [ ] No task requires knowledge from a future (not-yet-done) step
- [ ] Every entity in the design document has at least one task
- [ ] Auth/security is not left for the end (it should be Layer 4, not afterthought)
- [ ] Each task has a measurable done condition
- [ ] Total plan can be executed top-to-bottom without circular dependencies
- [ ] LLM Prompt Hints are specific, not vague ("Create User model with fields: id, email, passwordHash, createdAt" — good; "Create user stuff" — bad)

---

## Special Handling

### For API Design Documents specifically

Parse OpenAPI/REST structure:
- Group endpoints by resource (one task group per resource)
- Order: schema → service → route → validation → test
- Flag any endpoint that requires a non-trivial business rule as `COMPLEX`

### For Mobile / Frontend App Designs

Parse by screen/component:
- One task per screen or major component
- Separate: state management setup, navigation, API integration, UI polish

### For Microservice Architectures

Parse by service:
- One layer map per service
- Add inter-service contract tasks (define interfaces first)
- Flag shared libraries as `SHARED` — implement before consumers

---

## Reference

See `references/task-sizing-guide.md` for effort estimation examples.
See `references/llm-prompt-patterns.md` for LLM Prompt Hint templates.
