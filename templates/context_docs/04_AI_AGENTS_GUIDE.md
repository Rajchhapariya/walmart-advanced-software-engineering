# AI Agents Guide & Strict Behavioral Directives

**Target Models:** Claude 3.5 Sonnet, Gemini 1.5 Pro / Flash, GPT-4o, Cursor Agent, Antigravity Agent  
**Enforcement Level:** MANDATORY (Zero Hallucinations, Zero Broken Builds)

---

## 1. Absolute Zero Anti-Patterns (BANNED ACTIONS)

1. **NEVER assume missing API parameters or mock dependencies silently.** Always check active files and type signatures.
2. **NEVER use generic placeholder data or lorem ipsum.** Generate realistic, domain-accurate sample objects.
3. **NEVER overwrite complete files when making surgical modifications.** Always use precise line-targeted diffs.
4. **NEVER generate generic AI styling.** Strictly prohibit generic colors (plain `#ff0000`, `#00ff00`), harsh drop shadows, or un-padded layouts. Follow `02_DESIGN_SYSTEM.md`.
5. **NEVER install unapproved third-party dependencies** without checking existing virtualenv/node_modules first.

---

## 2. Code Generation Protocol

- **Strong Typing:** Every TypeScript function must have explicit parameter and return types (no `any`). In Python, strictly enforce Pydantic V2 models and `typing` hints.
- **Defensive Error Handling:** Wrap all external I/O, database calls, and network requests in robust try-catch blocks with descriptive error logging.
- **Verification First:** Before declaring a feature complete, run test suites (`pytest`, `npm test`) or execute a headless validation script to verify that code runs error-free.

---

## 3. Context Maintenance

- Read `01_PRD.md`, `02_DESIGN_SYSTEM.md`, and `03_ARCHITECTURE.md` before generating code.
- If a proposed change conflicts with existing architectural rules, flag the conflict immediately.
