---
name: task-executor
description: >
  Execute development tasks stored as files in a tasks/ folder structure (L0–L8 layers).
  Use this skill whenever the user wants to start or continue development from a file-based
  task plan, says "следующая задача", "запусти задачу", "что дальше", "сгенерируй промпт",
  "начни разработку", "выполни задачу", "задача готова", "отметь выполненной",
  "покажи прогресс", "start next task", "run task", "execute task", "mark done".
  Works with tasks/ directory where each layer is a subfolder (L0, L1...L8),
  each task is a separate .md file, and tasks/00-guide.md contains LLM execution rules.
  No external task managers needed.
---

# Task Executor — File-Based Dev Orchestrator

Runs development tasks from `tasks/L0`–`tasks/L8` folder structure.
Each task = one `.md` file. Progress tracked via `tasks/_progress.json`.

---

## Folder Structure Expected

```
tasks/
├── 00-guide.md           ← LLM execution guide — READ FIRST, ALWAYS
├── _progress.json        ← created by this skill, tracks status
├── L0/                   ← Foundation
│   ├── 01-init-project.md
│   └── 02-env-config.md
├── L1/                   ← Data Layer
├── L2/                   ← Business Logic
├── L3/                   ← API / Routes
├── L4/                   ← Auth
├── L5/                   ← Integrations
├── L6/                   ← Validation & Errors
├── L7/                   ← Tests
└── L8/                   ← Docs & Deploy
```

---

## CRITICAL: Always Read 00-guide.md First

**Before doing anything else in any mode**, read `tasks/00-guide.md`.

This file contains the author's execution rules, conventions, and constraints
that override any default behavior. Treat it as the system prompt for all
generated LLM prompts — it goes at the top of every prompt, verbatim.

If `00-guide.md` is missing → ask the user before proceeding:
"Файл tasks/00-guide.md не найден. Продолжить без него?"

---

## Step 0 — First Run Setup

If `tasks/_progress.json` does not exist:

1. **Read `tasks/00-guide.md`** — load and remember for this session
2. Scan all `tasks/L*/` folders, list every `.md` file
3. Parse each file — extract: title, depends_on, effort
4. Create `tasks/_progress.json`:

```json
{
  "project": "[infer from task content or 00-guide.md]",
  "created": "[ISO date]",
  "guide": "tasks/00-guide.md",
  "tasks": {
    "L0/01-init-project.md": {
      "title": "Init project & env config",
      "layer": 0,
      "effort": "S",
      "depends_on": [],
      "status": "READY",
      "completed_output": null
    },
    "L1/01-user-schema.md": {
      "title": "Create User schema & migration",
      "layer": 1,
      "effort": "S",
      "depends_on": ["L0/01-init-project.md"],
      "status": "BLOCKED",
      "completed_output": null
    }
  }
}
```

Status rules on init:
- No `depends_on` → `READY`
- Has unfinished `depends_on` → `BLOCKED`

---

## MODE: NEXT — What to Work on Now

Triggered by: "следующая задача", "что дальше", "start next task"

1. Read `tasks/00-guide.md`
2. Read `tasks/_progress.json`
3. Find all tasks with status `READY`
4. Pick by priority: lowest layer first → smallest effort first
5. Read the task `.md` file
6. Display:

```
🎯 NEXT: L[N]/[filename]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[full task content from .md file]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Effort: [size]  |  Layer: [name]
```

Then ask: "Сгенерировать промпт для этой задачи?"

---

## MODE: PROMPT — Generate LLM Prompt

Triggered by: "сгенерируй промпт", "generate prompt", or after NEXT

### Step 1 — Load guide and task

- Read `tasks/00-guide.md` (full content)
- Read the target task `.md` file (full content)

### Step 2 — Collect missing context from user

Ask only what's NOT already covered by 00-guide.md or the task file:
- Previous task output (paste the code/schema/result produced)

### Step 3 — Build the prompt

```
=== EXECUTION GUIDE (follow strictly) ===
[full content of tasks/00-guide.md — verbatim, unmodified]

=== PREVIOUS STEP OUTPUT (context — do not rewrite) ===
[user-provided output from last completed task]

=== YOUR TASK: [task title] ===
[full content of the task .md file]

=== REMINDER ===
- Return complete, runnable code only
- No placeholders, no TODO comments
- Follow the exact output and done-condition specified above
```

Output the prompt in a fenced code block — ready to copy-paste into Claude Code / Cursor / Copilot.

Update `_progress.json`: set this task's status to `IN_PROGRESS`.

See `references/prompt-patterns.md` for task-type-specific structural templates.

---

## MODE: DONE — Mark Task Complete

Triggered by: "задача готова", "выполнено", "mark done", "отметь выполненной"

1. Ask: "Какую задачу отмечаем? (или текущую IN_PROGRESS?)"
2. Ask: "Вставь краткое описание результата (1–2 строки): что было создано?"
3. Update `_progress.json`:
   - Set task status → `DONE`
   - Set `completed_output` → user's summary
4. Dependency resolution:
   - Find all BLOCKED tasks that list this task in `depends_on`
   - For each: if ALL their `depends_on` are DONE → set status `READY`
5. Write updated `_progress.json`
6. Report:

```
✅ Done: [task title]
🔓 Unlocked: [newly READY tasks, or "none yet"]

Progress: [X]/[total] done
🟢 Ready now: [list]
```

---

## MODE: PROGRESS — Show Current State

Triggered by: "покажи прогресс", "сколько осталось", "статус"

```
📊 Progress: ████████░░░░  X/Y done ([%]%)

✅ DONE ([n]):
  L0/01 — Init project
  ...

🔄 IN PROGRESS:
  L1/01 — User schema

🟢 READY ([n]):
  L1/02 — Product schema

🔒 BLOCKED ([n]):
  L3/01 — POST /users  (waiting: L2/01)
```

---

## Key Rules

1. **Always read `00-guide.md` before generating any prompt** — it overrides defaults
2. **`00-guide.md` goes verbatim at the top of every LLM prompt** — never summarize it
3. **Never generate a prompt for a BLOCKED task** — warn user, show what's blocking it
4. **Always include previous task output as context** — LLMs have no memory between prompts
5. **One task = one prompt** — never batch multiple `.md` files into one prompt
6. **After DONE → always show what got unlocked** to keep momentum
7. **If effort = L** → warn: "Эта задача большая. Хочешь разбить её на подшаги?"
8. **`_progress.json` is the source of truth** — always read fresh, always write after changes

---

## References

- `references/prompt-patterns.md` — LLM prompt templates per task type
- `references/status-flow.md` — Status state machine & dependency resolution
