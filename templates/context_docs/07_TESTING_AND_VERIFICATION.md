# Testing & Verification Strategy

**Frameworks:** Pytest (Backend) | Vitest / Playwright (Frontend & E2E)  
**Target Coverage:** > 80% Core Domain Logic

---

## 1. Test Pyramid & Execution Tiers

1. **Unit Tests:** Fast, isolated tests for utility functions, algorithmic processors, and Pydantic validators.
2. **Integration Tests:** Tests against real PostgreSQL test databases (using testcontainers or transactional rollbacks).
3. **End-to-End (E2E) Browser Tests:** Automated headless Playwright runs that capture screenshots and verify DOM states.

---

## 2. Pre-Flight Verification Checklist

Before submitting or merging any task:

- [ ] Run linter & formatter (`ruff check .` or `eslint .`)
- [ ] Run unit test suite (`pytest tests/`)
- [ ] Validate database migrations (`alembic upgrade head`)
- [ ] Check security vulnerabilities (`pip-audit` or `npm audit`)
- [ ] Run headless browser screenshot verification to inspect UI rendering visually.
